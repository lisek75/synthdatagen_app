import os
import gradio as gr
import threading
from src.synth_data_gen import SynthDataGen

generator = SynthDataGen()

# Update the output format choices based on the selected dataset type
def update_output_format(dataset_type):
    if dataset_type in ["Tabular", "Time-series"]:
        return gr.update(choices=["JSON", "csv", "Parquet"], value="JSON")
    elif dataset_type == "Text":
        return gr.update(choices=["JSON", "Markdown"], value="JSON")

def update_pipeline(business_problem, dataset_type, output_format, num_samples, model):
    # Check if business problem is empty
    if not business_problem.strip():
        yield [gr.update(visible=False), gr.update(visible=True), "❌ Please enter a business problem before generating."]
        return

    # Initial feedback while generating
    yield [gr.update(visible=False), gr.update(visible=False), "⏳ Generating dataset..."]

    try:
        # Pack inputs into a dictionary for the generator
        input_data = {
            "business_problem": business_problem,
            "dataset_type": dataset_type,
            "output_format": output_format,
            "num_samples": num_samples,
            "model": model
        }

        # Generate dataset file
        file_path = generator.generate_dataset(**input_data)
        print("🧪 File result returned:", file_path)

        # Check if file exists and return success message + file path
        if isinstance(file_path, str) and os.path.exists(file_path):
            threading.Timer(60, os.remove, args=[file_path]).start()  # Auto-delete after 60s
            yield [gr.update(value=file_path, visible=True), gr.update(visible=True), "✅ Dataset ready for download."]
        else:
            # Handle invalid or missing file
            yield [gr.update(visible=False), gr.update(visible=True), "❌ Error: File not created or path invalid."]
    
    except Exception as e:
        # Catch and display any errors in the pipeline
        yield [gr.update(visible=False), gr.update(visible=True), f"❌ Pipeline error: {e}"]

def build_ui(css_path="assets/styles.css"):
    with open(css_path, "r") as f:
        css = f.read()

    with gr.Blocks(css=css, title="🧬SynthDataGen") as ui:
        with gr.Column(elem_id="app-container"):
            gr.Markdown("<h1 id='app-title'>SynthDataGen 🧬 </h1>")
            gr.Markdown("<h2 id='app-subtitle'>AI-Powered Synthetic Dataset Generator</h2>")

            gr.HTML("""
            <div id="intro-text">
                <p>With SynthDataGen, easily generate <strong>diverse datasets in different formats</strong> for testing, development, and AI training.</p>
                <h4>🎯 How It Works:</h4>
                <ol>
                <li>1️⃣ Define your business problem or dataset topic.</li>
                <li>2️⃣ Select the dataset type, output format, model, and number of samples.</li>
                <li>3️⃣ Receive your synthetic dataset — ready to download and use!</li>
                </ol>
            </div>
            """)

            gr.HTML("""
                <div id="learn-more-button">
                    <a href="https://github.com/lisek75/synthdatagen_app/blob/main/README.md" class="button-link" target="_blank">Learn More</a>
                </div>
                """)

            gr.Markdown("""
                <p><strong>🧠 Need inspiration?</strong> Try one of these examples:</p>
                <ul>
                <li>Movie summaries for genre classification.</li>
                <li>Generate customer chats with realistic dialogue, chat_id, timestamp, names, sentiment label, and aligned transcript.</li>
                <li>Create daily stock prices for 2 companies with typical fields like date, ticker, open, close, high, low, and volume.</li>
                </ul>
                """)

            gr.Markdown("<p><strong>Start generating your synthetic datasets now!</strong> 🗂️✨</p>")

            with gr.Group(elem_id="input-container"):

                business_problem = gr.Textbox(
                    placeholder="Describe the dataset you want (e.g., Job postings, Customer reviews, Sensor data, Movie titles)",
                    lines=2,
                    label="📌 Business Problem",
                    elem_classes=["label-box"],
                    elem_id="business-problem-box"
                )

                with gr.Row(elem_classes="column-gap"):
                    with gr.Column(scale=1):
                        dataset_type = gr.Dropdown(
                            ["Tabular", "Time-series", "Text"],
                            value="Tabular",
                            label="📊 Dataset Type",
                            elem_classes=["label-box"],
                            elem_id="custom-dropdown"
                        )

                    with gr.Column(scale=1):
                        output_format = gr.Dropdown(
                            choices=["JSON", "csv", "Parquet"], 
                            value="JSON",
                            label="📁 Output Format",
                            elem_classes=["label-box"],
                            elem_id="custom-dropdown"
                        )

                    # Bind the update function to the dataset type dropdown
                    dataset_type.change(
                        update_output_format,
                        inputs=[dataset_type],
                        outputs=[output_format]
                    )

                with gr.Row(elem_classes="row-spacer column-gap"):
                    with gr.Column(scale=1):
                        model = gr.Dropdown(
                            ["GPT", "Claude"],
                            value="GPT",
                            label="🤖 Model",
                            elem_classes=["label-box"],
                            elem_id="custom-dropdown"
                        )

                    with gr.Column(scale=1):
                        num_samples = gr.Slider(
                            minimum=10,
                            maximum=1000,
                            value=10,
                            step=1,
                            interactive=True,
                            label="🔢 Number of Samples",
                            elem_classes=["label-box"]
                        )

            # Hidden file component for dataset download
            file_download = gr.File(visible=False, elem_id="download-box", label=None)

            # Component to display status messages
            status_message = gr.Markdown("", label="Status")

            # Button to trigger dataset generation
            run_btn = gr.Button("Create a dataset", elem_id="run-btn")
            run_btn.click(
                update_pipeline,
                inputs=[business_problem, dataset_type, output_format, num_samples, model],
                outputs=[file_download, run_btn, status_message]
            )

    return ui # Return the complete UI
