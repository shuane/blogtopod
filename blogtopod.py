# /// script
# requires-python = ">=3.12,<=3.13"
# dependencies = [
#     "marimo",
#     "gaspare==0.3.3",
#     "openai==1.78.1",
#     "pydub==0.25.1",
#     "contextkit==0.0.6",
# ]
# ///

import marimo

__generated_with = "0.11.31"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import os
    from openai import OpenAI
    import gaspare as gp
    import unicodedata
    import re
    from pathlib import Path
    from contextkit.read import read_url
    from io import BytesIO
    from pydub import AudioSegment
    return (
        AudioSegment,
        BytesIO,
        OpenAI,
        Path,
        gp,
        mo,
        os,
        re,
        read_url,
        unicodedata,
    )


@app.cell
def _(mo):
    mo.md(
        r"""
        **Note**: This script assumes you have your OPENAI_API_KEY and GEMINI_API_KEY environment variables set

        - Gemini is used for making the script
        - OpenAI is used for the voices
        """
    )
    return


@app.cell
def _(OpenAI):
    client = OpenAI()
    return (client,)


@app.cell
def _(mo):
    input_url = mo.ui.text(label="URL", value="https://medium.com/@pol.avec/ai-is-the-new-ui-generative-ui-with-fasthtml-e8cfcc98e5b5", full_width=True)
    output_file = mo.ui.text(label="Output file", value="pol_pod.mp3", full_width=True)
    hosts = [mo.ui.text(label="First host", value="Alex"), mo.ui.text(label="Second host", value="Jamie")]
    voices = [mo.ui.text(label="First voice", value="fable"), mo.ui.text(label="Second voice", value="shimmer")]


    run_button = mo.ui.run_button(label="Run!")

    mo.md(f"""
    {input_url}

    {output_file}

    {hosts[0]} {voices[0]}

    {hosts[1]} {voices[1]}

    Note that you can find/test voices at https://www.openai.fm/

    {run_button}
    """)
    return hosts, input_url, output_file, run_button, voices


@app.cell(hide_code=True)
def _(re, unicodedata):
    # functions
    def clean_text_for_tts(text):


        # Replace specific problematic characters
        replacements = {
            'â¦': '...',  # Fix broken ellipsis
            'â¦': '...',  # Fix broken ellipsis2
            'â': "'",     # Fix apostrophes
            'â': '"',     # Fix quotes
            'â': '"',     # Fix quotes
            '\u200b': '', # Remove zero-width spaces
        }

        for old, new in replacements.items():
            text = text.replace(old, new)

        # Clean up any remaining non-standard characters
        text = re.sub(r'[^\x00-\x7F]+', ' ', text)

        # Fix multiple spaces
        text = re.sub(r' +', ' ', text)

        # Normalize Unicode characters
        text = unicodedata.normalize('NFKD', text)    

        return text.strip()


    def parse_podcast_script(script_text, s1, s2):
        lines = script_text.strip().split('\n')
        segments = []
        current_speaker = None
        current_text = ""

        for line in lines:
            line = line.strip()
            if not line:
                continue

            if line.startswith(f"{s1.upper()}:") or line.startswith(f"{s2.upper()}:"):
                # Save previous segment if exists
                if current_speaker:
                    segments.append({"speaker": current_speaker, "text": clean_text_for_tts(current_text.strip())})

                # Start new segment
                current_speaker = line.split(':')[0]
                current_text = line[len(current_speaker)+1:].strip()
            else:
                pass
                # Commenting out the following because I do not want to continue current segment if not marked for a speaker
                # current_text += " " + line

        # Add the last segment
        if current_speaker:
            segments.append({"speaker": current_speaker, "text": clean_text_for_tts(current_text.strip())})

        return segments
    return clean_text_for_tts, parse_podcast_script


@app.cell
def _():
    # with open("/home/dum/Code/pol_post.md", "r") as fr:
    #     post = fr.read()

    # segments = parse_podcast_script(script, hosts[0].value, hosts[1].value)
    # len(segments)
    return


@app.cell
def _(input_url, read_url):
    page = read_url(input_url.value)
    print(page)
    return (page,)


@app.cell
def _(hosts, page):
    prompt = f"""
    Please transform the following source material into an engaging podcast script with two hosts named {hosts[0].value} and {hosts[1].value}. 

    SOURCE MATERIAL:
    ----
    {page}
    ----


    INSTRUCTIONS:
    ----
    1. Format the output as a ready-to-record script with clear speaker labels.
    2. Create distinct personalities for each host:
       - {hosts[0].value}: Enthusiastic, curious, asks clarifying questions, brings energy
       - {hosts[1].value}: Analytical, thoughtful, provides context and deeper insights

    3. Structure the conversation to include:
       - A natural introduction where hosts welcome listeners and preview the topic
       - The main discussion that breaks down complex points into digestible segments
       - Natural transitions between subtopics with occasional light banter
       - A conclusion that summarizes key points and possibly mentions what's coming next

    4. Writing style guidelines:
       - Use conversational language appropriate for audio (shorter sentences, clear pronunciation)
       - Include verbal transitions and hand-offs between hosts
       - Add occasional personal anecdotes, questions, or reactions that feel authentic
       - Include 2-3 moments of genuine interaction (friendly disagreement, humor, or surprise)
       - Vary sentence structures and pacing to maintain listener interest

    5. Keep the total length to approximately 25 minutes of speaking time.

    6. Please format the output with consistent speaker labels that can be easily parsed:

    {hosts[0].value.upper()}: [{hosts[0].value}'s dialogue here]

    {hosts[1].value.upper()}: [{hosts[1].value}'s dialogue here]

    Use exactly this format with the name in all caps followed by a colon, then the complete text for that turn. Always start each speaker's part on a new line.

    7. The final script should read like an authentic conversation while effectively communicating all the key information from the source material.

    """
    return (prompt,)


@app.cell
def _(gp, hosts, mo, parse_podcast_script, prompt, run_button):
    # Generate script if Run! button has been clicked
    mo.stop(not run_button.value)
    chat = gp.Chat(model="gemini-2.5-pro-preview-03-25")
    script = chat(prompt).text
    segments = parse_podcast_script(script, hosts[0].value, hosts[1].value)
    len(segments)
    return chat, script, segments


@app.cell
def _(AudioSegment, BytesIO, client, hosts, mo, run_button, segments, voices):
    # Gather voice segments if Run~ button has been clicked
    mo.stop(not run_button.value)

    parts = []
    for s in segments:
        with client.audio.speech.with_streaming_response.create(
            model="gpt-4o-mini-tts",
            voice=voices[0].value if s['speaker'] == hosts[0].value.upper() else voices[1].value,
            input=s['text'],
            instructions="You are a podcast host with these qualities: Enthusiastic, curious, asks clarifying questions, brings energy" if s['speaker'] == voices[0].value.upper() else "You are a podcast host with these qualities: Analytical, thoughtful, provides context and deeper insights",
         ) as response:
            buffer = BytesIO()
            for chunk in response.iter_bytes():
                buffer.write(chunk)
            buffer.seek(0)
            parts.append(AudioSegment.from_file(buffer, format="mp3"))

    len(parts)
    return buffer, chunk, parts, response, s


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Audio preview""")
    return


@app.cell
def _(AudioSegment, mo, parts, run_button):
    mo.stop(not run_button.value)
    preview = sum(parts, AudioSegment.empty())
    preview
    return (preview,)


@app.cell
def _(Path, output_file, preview):
    preview.export(Path(output_file.value))
    print(f"Wrote to {output_file.value}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""# Script""")
    return


@app.cell(hide_code=True)
def _(clean_text_for_tts, output_file, script):
    with open(output_file.value.replace(".mp3", "_script.md"), "w") as fw:
        fw.write(clean_text_for_tts(script))
    return (fw,)


@app.cell(hide_code=True)
def _(clean_text_for_tts, script):
    print(clean_text_for_tts(script))
    return


if __name__ == "__main__":
    app.run()
