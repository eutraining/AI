import gradio as gr
import io


def decode_file_content(file):
    # Create a BytesIO object and write the binary data to it
    bytes_io = io.BytesIO(file)
    # Read and manipulate the binary data
    read_binary_data = bytes_io.read()
    return read_binary_data.decode('utf-8')


# Function to process the inputs and return a result
def process_input(file1, file2, text_input):
    # Decode file content
    file1 = decode_file_content(file1)
    file2 = decode_file_content(file2)
    result = f"File 1: {file1}\nFile 2: {file2}\nText Input: {text_input}"
    return result


# Define the interface
iface = gr.Interface(
    fn=process_input,  # Function to call for processing
    inputs=[
        gr.File(type='binary'),  # First file input
        gr.File(type='binary'),  # Second file input
        gr.Textbox(lines=2, placeholder="Name Here..."),  # Text input
    ],
    outputs="text"  # Output type
)

# Launch the interface on a local server
iface.launch(share=True)
