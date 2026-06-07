import streamlit as st
import time
import logging
import threading
from services.config.workout_config import METRICS_FIELDS
from services.persistence.exercise_repository import add_exercise

logger = logging.getLogger(__name__)


def _run_voice_in_background(pipeline, event, exercise, metrics):
    try:
        result = pipeline.process_event(event, exercise, metrics)
        if result:
            pipeline._pending_result = result
    except Exception as e:
        logger.error(f"Background voice pipeline error: {e}")


def _trigger_voice(pipeline, event, exercise, metrics):
    if not pipeline:
        return
    
    if getattr(pipeline, '_voice_thread', None) and pipeline._voice_thread.is_alive():
        return

    pipeline._pending_result = None
    t = threading.Thread(
        target=_run_voice_in_background,
        args=(pipeline, event, exercise, metrics),
        daemon=True,
    )
    pipeline._voice_thread = t
    t.start()


def _collect_voice_result(pipeline):
    """Check if background voice thread has a result and apply it to session state."""
    if not pipeline:
        return
    
    result = getattr(pipeline, '_pending_result', None)
    if result:
        pipeline._pending_result = None
        voice, text = result
        st.session_state.audio_to_play = voice
        st.session_state.coach_feedback = text


def sync_metrics_update(context):
    if not context or not hasattr(context, "state") or not context.state.playing:
        return
    
    processor = getattr(context, "video_processor", None)

    if not processor:
        return 
    
    exercise = st.session_state.get("exercise_type")

    if not exercise:
        return
    
    processor.set_exercise(exercise)
    latest_metrics = processor.get_latest_metrics()

    if not latest_metrics:
        return
    
    reps = latest_metrics.get("reps", 0)

    if reps is None:
        reps = 0
        
    st.session_state.reps = reps

    fields = METRICS_FIELDS.get(exercise)

    if not fields:
        return 

    for key, default in fields.items():
        st.session_state[key] = latest_metrics.get(key, default)

    reps_per_set = st.session_state.get("reps_per_set", 0)
    target_sets = st.session_state.get("target_sets", 0)

    if reps is not None and reps_per_set > 0 and target_sets > 0:
        sets_completed = reps // reps_per_set
        current_set_reps = reps % reps_per_set
        workout_completed = sets_completed >= target_sets 
    else:
        sets_completed = 0
        current_set_reps = 0
        workout_completed = False

    st.session_state.sets_completed = sets_completed
    st.session_state.current_set_reps = current_set_reps
    st.session_state.workout_completed = workout_completed

    pipeline = st.session_state.get("voice_pipeline")

    _collect_voice_result(pipeline)

    last_saved_sets = st.session_state.get("last_saved_sets_completed", 0)

    if target_sets > 0 and reps_per_set > 0 and sets_completed > last_saved_sets:
        newly_completed = sets_completed - last_saved_sets
        now_ts = time.time()
        started_at = st.session_state.get("set_cycle_started_at", now_ts)
        time_taken = now_ts - started_at
        user_id = st.session_state.get("user_id", 0)

        add_exercise(user_id, exercise, newly_completed * reps_per_set, newly_completed, time_taken)

        _trigger_voice(pipeline, "set_completed", exercise, latest_metrics)

        st.session_state.set_cycle_started_at = now_ts
        st.session_state.last_saved_sets_completed = sets_completed

    if workout_completed and not st.session_state.get("last_notified_workout_complete", False):
        st.session_state.last_notified_workout_complete = True
        _trigger_voice(pipeline, "workout_completed", exercise, latest_metrics)
                
    pose_detected = latest_metrics.get("pose_detected", True)
    
    if not pose_detected:
        _trigger_voice(
            pipeline,
            "no_pose_detected",
            exercise,
            {"issue": "No pose detected! Please step into the camera frame."},
        )

    _trigger_voice(pipeline, "ongoing_form_check", exercise, latest_metrics)
