import streamlit as st
import json
import time
from pathlib import Path
from utils.model_manager import (
    find_free_port,
    save_model_file,
    save_server_script,
    save_base_request,
    start_model_server,
    stop_model_server,
    check_server_health,
    make_prediction,
    update_base_request,
    delete_model,
    get_available_models,
    get_model_logs
)


def show():
    st.header("Model Management")
    st.write("Prepare and manage your ML models for predictions using FastMLAPI library.")

    if 'running_models' not in st.session_state:
        st.session_state['running_models'] = {}

    if 'prepare_step' not in st.session_state:
        st.session_state['prepare_step'] = 1

    if 'uploaded_model_file' not in st.session_state:
        st.session_state['uploaded_model_file'] = None

    if 'uploaded_server_file' not in st.session_state:
        st.session_state['uploaded_server_file'] = None

    if 'uploaded_request_file' not in st.session_state:
        st.session_state['uploaded_request_file'] = None

    if 'model_name_for_deploy' not in st.session_state:
        st.session_state['model_name_for_deploy'] = None

    tab1, tab2, tab3 = st.tabs([
        "🚀 Prepare & Run",
        "🔮 Predict" if st.session_state['running_models'] else "🔮 Predict (Deploy model first)",
        "⚙️ Manage"
    ])

    with tab1:
        st.subheader("Prepare and Deploy Model")

        progress_text = f"Step {st.session_state['prepare_step']} of 4"
        st.progress(st.session_state['prepare_step'] / 4, text=progress_text)

        st.markdown("---")


        st.write("**Step 1: Upload Model (.pkl file)**")
        uploaded_model = st.file_uploader(
            "Upload .pkl model file:",
            type=['pkl'],
            key="mm_upload_model"
        )

        if uploaded_model:
            st.session_state['uploaded_model_file'] = uploaded_model

            custom_name = st.text_input(
                "Model name (optional - leave empty to use filename):",
                key="mm_model_custom_name"
            )

            if st.button("✅ Confirm Model", type="primary", key="mm_confirm_model"):
                st.session_state['model_name_for_deploy'] = custom_name if custom_name else uploaded_model.name.replace('.pkl', '')
                st.session_state['prepare_step'] = 2
                st.success(f"✅ Model '{st.session_state['model_name_for_deploy']}' ready!")
                st.rerun()

        if st.session_state['prepare_step'] >= 2 and st.session_state['model_name_for_deploy']:
            st.info(f"✅ Model ready: {st.session_state['model_name_for_deploy']}.pkl")

        st.markdown("---")

        if st.session_state['prepare_step'] >= 2:
            st.write("**Step 2: Upload Server Script (.py file)**")
            st.info("📝 Server script must follow FastMLAPI structure (MLController with load_model method)")

            uploaded_server = st.file_uploader(
                f"Upload server script for '{st.session_state['model_name_for_deploy']}':",
                type=['py'],
                key="mm_upload_server"
            )

            if uploaded_server:
                st.session_state['uploaded_server_file'] = uploaded_server

                if st.button("✅ Confirm Server Script", type="primary", key="mm_confirm_server"):
                    st.session_state['prepare_step'] = 3
                    st.success("✅ Server script ready!")
                    st.rerun()

            if st.session_state['prepare_step'] >= 3:
                st.info("✅ Server script ready")

        st.markdown("---")

        if st.session_state['prepare_step'] >= 3:
            st.write("**Step 3: Upload Base Request (JSON file)**")
            st.info("📝 Base request JSON will be used as default payload for predictions")

            uploaded_request = st.file_uploader(
                f"Upload base request for '{st.session_state['model_name_for_deploy']}':",
                type=['json'],
                key="mm_upload_request"
            )

            if uploaded_request:
                st.session_state['uploaded_request_file'] = uploaded_request

                if st.button("✅ Confirm Base Request", type="primary", key="mm_confirm_request"):
                    st.session_state['prepare_step'] = 4
                    st.success("✅ Base request ready!")
                    st.rerun()

            if st.session_state['prepare_step'] >= 4:
                st.info("✅ Base request ready")

        st.markdown("---")

        if st.session_state['prepare_step'] >= 4:
            st.write("**Step 4: Save & Deploy Model Server**")

            suggested_port = find_free_port()
            port = st.number_input(
                "Port:",
                min_value=8000,
                max_value=9999,
                value=suggested_port if suggested_port else 8000,
                key="mm_deploy_port"
            )

            if st.button("💾 Save & Deploy Server", type="primary", key="mm_deploy_button"):
                with st.spinner("Saving files and starting server..."):
                    try:
                        model_name = st.session_state['model_name_for_deploy']

                        model_path = save_model_file(st.session_state['uploaded_model_file'], model_name)
                        st.success(f"✅ Saved: {model_path}")

                        server_path = save_server_script(st.session_state['uploaded_server_file'], model_name)
                        st.success(f"✅ Saved: {server_path}")

                        request_path = save_base_request(st.session_state['uploaded_request_file'], model_name)
                        st.success(f"✅ Saved: {request_path}")

                        pid, success, error_msg = start_model_server(model_name, port)

                        if success:
                            st.session_state['running_models'][model_name] = {
                                'port': port,
                                'pid': pid,
                                'status': 'running'
                            }
                            st.success(f"🚀 Server running on port {port}!")
                            st.info(f"📖 API Docs: http://127.0.0.1:{port}/docs")

                            st.session_state['prepare_step'] = 1
                            st.session_state['uploaded_model_file'] = None
                            st.session_state['uploaded_server_file'] = None
                            st.session_state['uploaded_request_file'] = None
                            st.session_state['model_name_for_deploy'] = None

                            st.balloons()
                            time.sleep(2)
                            st.rerun()
                        else:
                            st.error("❌ Failed to start server!")
                            st.error(f"**Details:**")
                            st.code(error_msg, language="text")
                            st.info("💡 Check the log files in `models/logs/` directory for more details")

                    except Exception as e:
                        st.error(f"❌ Error: {e}")
        else:
            st.info("ℹ️ Complete steps 1-3 to enable deployment")

    with tab2:
        st.subheader("Make Predictions")

        running = st.session_state.get('running_models', {})

        if not running:
            st.warning("⚠️ No models running. Deploy a model first in 'Prepare & Run' tab.")
            return

        model_options = list(running.keys())
        selected_predict_model = st.selectbox(
            "Select model:",
            model_options,
            key="mm_predict_model_select"
        )

        model_info = running[selected_predict_model]
        port = model_info['port']

        is_healthy = check_server_health(port)

        if is_healthy:
            st.success(f"🟢 Model '{selected_predict_model}' is running on port {port}")
        else:
            st.error(f"🔴 Model server not responding!")
            return

        st.markdown("---")

        base_request_path = Path("models") / "requests" / f"model_{selected_predict_model}_base_request.json"

        if base_request_path.exists():
            with open(base_request_path, 'r') as f:
                base_request = json.load(f)

            st.write("**Base Request:**")
            st.json(base_request)

            st.write("**Edit Request (optional):**")
            custom_request = st.text_area(
                "Modify request JSON:",
                value=json.dumps(base_request, indent=2),
                height=200,
                key="mm_custom_request"
            )

            if st.button("🔮 Make Prediction", type="primary", key="mm_predict_button"):
                try:
                    custom_data = json.loads(custom_request)

                    result = make_prediction(port, base_request_path, custom_data)

                    if result['success']:
                        st.success("✅ Prediction completed!")
                        st.subheader("Response:")
                        st.json(result['data'])
                    else:
                        st.error(f"❌ Prediction failed!")
                        st.code(result['error'])

                except json.JSONDecodeError:
                    st.error("❌ Invalid JSON format!")

        else:
            st.warning(f"⚠️ Base request not found for '{selected_predict_model}'.")

            st.write("**Manual Request:**")
            manual_request = st.text_area(
                "Enter request JSON:",
                value='{"data": [[1.0], [2.0], [3.0]]}',
                height=200,
                key="mm_manual_request"
            )

            if st.button("🔮 Make Prediction", type="primary", key="mm_predict_manual_button"):
                try:
                    custom_data = json.loads(manual_request)

                    url = f"http://127.0.0.1:{port}/predict"
                    import requests
                    response = requests.post(url, json=custom_data, timeout=10)

                    if response.status_code == 200:
                        st.success("✅ Prediction completed!")
                        st.subheader("Response:")
                        st.json(response.json())
                    else:
                        st.error(f"❌ Prediction failed!")
                        st.code(response.text)

                except json.JSONDecodeError:
                    st.error("❌ Invalid JSON format!")
                except Exception as e:
                    st.error(f"❌ Error: {e}")

    with tab3:
        st.subheader("Manage Models")

        all_models = get_available_models()

        if not all_models:
            st.info("ℹ️ No models available.")
        else:
            for model_name in all_models:
                with st.expander(f"📦 {model_name}", expanded=True):
                    col1, col2, col3 = st.columns([2, 1, 1])

                    with col1:
                        is_running = model_name in st.session_state.get('running_models', {})

                        if is_running:
                            port = st.session_state['running_models'][model_name]['port']
                            st.write(f"**Status:** 🟢 Running on port {port}")
                            st.write(f"[📖 API Docs](http://127.0.0.1:{port}/docs)")
                        else:
                            st.write(f"**Status:** 🔴 Not running")

                        models_dir = Path("models")
                        model_file = models_dir / f"{model_name}.pkl"
                        server_file = models_dir / "servers" / f"model_{model_name}_server.py"
                        request_file = models_dir / "requests" / f"model_{model_name}_base_request.json"

                        st.write(f"**Files:**")
                        st.write(f"- Model: {'✅' if model_file.exists() else '❌'} {model_name}.pkl")
                        st.write(f"- Server: {'✅' if server_file.exists() else '❌'} model_{model_name}_server.py")
                        st.write(f"- Request: {'✅' if request_file.exists() else '❌'} model_{model_name}_base_request.json")

                    with col2:
                        st.write("**Actions:**")

                        if is_running:
                            if st.button("📋 View Logs", key=f"mm_logs_{model_name}"):
                                st.session_state[f'show_logs_{model_name}'] = True

                        if request_file.exists():
                            if st.button("📝 Edit Request", key=f"mm_edit_{model_name}"):
                                st.session_state[f'edit_request_{model_name}'] = True

                        if is_running:
                            if st.button("⏹️ Stop Server", key=f"mm_stop_{model_name}"):
                                pid = st.session_state['running_models'][model_name]['pid']
                                if stop_model_server(pid):
                                    del st.session_state['running_models'][model_name]
                                    st.success("✅ Server stopped!")
                                    st.rerun()
                                else:
                                    st.error("❌ Failed to stop server!")

                    with col3:
                        st.write("")
                        st.write("")
                        if st.button("🗑️ Delete", key=f"mm_delete_{model_name}"):
                            pid = None
                            if is_running:
                                pid = st.session_state['running_models'][model_name]['pid']

                            if delete_model(model_name, pid):
                                if is_running:
                                    del st.session_state['running_models'][model_name]
                                st.success(f"✅ Model '{model_name}' deleted!")
                                st.rerun()
                            else:
                                st.error("❌ Failed to delete model!")

                    if st.session_state.get(f'show_logs_{model_name}', False) and is_running:
                        st.markdown("---")
                        st.write("**📋 Server Logs:**")

                        port = st.session_state['running_models'][model_name]['port']
                        logs = get_model_logs(model_name, port)

                        tab_stdout, tab_stderr = st.tabs(["Standard Output", "Error Output"])

                        with tab_stdout:
                            if logs['stdout_exists']:
                                if logs['stdout']:
                                    st.code(logs['stdout'], language="text")
                                else:
                                    st.info("Log file is empty")
                            else:
                                st.warning("Log file not found")

                        with tab_stderr:
                            if logs['stderr_exists']:
                                if logs['stderr']:
                                    st.code(logs['stderr'], language="text")
                                else:
                                    st.info("Error log is empty (no errors)")
                            else:
                                st.warning("Error log not found")

                        if st.button("❌ Close Logs", key=f"mm_close_logs_{model_name}"):
                            st.session_state[f'show_logs_{model_name}'] = False
                            st.rerun()

                    if st.session_state.get(f'edit_request_{model_name}', False):
                        st.markdown("---")
                        st.write("**Edit Base Request:**")

                        with open(request_file, 'r') as f:
                            current_request = json.load(f)

                        edited_request = st.text_area(
                            "Request JSON:",
                            value=json.dumps(current_request, indent=2),
                            height=200,
                            key=f"mm_edit_area_{model_name}"
                        )

                        col_save, col_cancel = st.columns([1, 1])
                        with col_save:
                            if st.button("💾 Save", key=f"mm_save_edit_{model_name}"):
                                try:
                                    new_data = json.loads(edited_request)
                                    if update_base_request(model_name, new_data):
                                        st.success("✅ Request updated!")
                                        st.session_state[f'edit_request_{model_name}'] = False
                                        st.rerun()
                                    else:
                                        st.error("❌ Failed to update!")
                                except json.JSONDecodeError:
                                    st.error("❌ Invalid JSON!")

                        with col_cancel:
                            if st.button("❌ Cancel", key=f"mm_cancel_edit_{model_name}"):
                                st.session_state[f'edit_request_{model_name}'] = False
                                st.rerun()

