from src.ui import build_ui

if __name__ == "__main__":
    # Build the user interface
    ui = build_ui()
    
    # Launch the UI in the browser with access to the "output" folder
    ui.launch(
        inbrowser=True,
        allowed_paths=["output"],
        server_name="0.0.0.0",
        server_port=7860
    )

