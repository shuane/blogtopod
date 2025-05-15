# blogtopod: Turn blog posts into podcast episodes

*Convert blog posts into podcast episodes using AI text-to-speech—because sometimes you'd rather listen than read.*

## How to install and run

This tool requires Python 3.12. You have two options for running it:

### Option 1: Using `uv` (recommended)

First install [uv](https://github.com/astral-sh/uv), the modern Python package installer:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then run the application directly:

```bash
uv run --python 3.12 https://raw.githubusercontent.com/shuane/blogtopod/refs/heads/main/blogtopod.py
```

The beauty of `uv` is that it handles all dependency management automatically—the requirements are built right into the Python file.

### Option 2: Traditional pip install

If you prefer using your existing Python environment:

```bash
pip install -r requirements.txt
python blogtopod.py
```

## API Keys Required

This tool uses both OpenAI and Google's Gemini for text-to-speech generation. You'll need to provide API keys for both services:

### Getting your OpenAI API key

1. Go to [platform.openai.com](https://platform.openai.com/)
2. Sign up or log in to your account
3. Click on your profile picture → "View API keys"
4. Click "Create new secret key" and copy it

### Getting your Google Gemini API key

1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Click "Get API key" in the sidebar
4. Create a new API key and copy it

### Setting up your environment

Set up environment variables before running, you could do this in bash or by loading it in ~/.bashrc:

```bash
export OPENAI_API_KEY=your_openai_key_here
export GEMINI_API_KEY=your_gemini_key_here
```

## What does this do?

`blogtopod` converts blog posts into podcast episodes by:

1. Fetching the content of a blog post URL
2. Calling Gemini 2.5 Pro to make a podcast script
3. Using OpenAI text-to-speech to generate natural sounding audio
4. Outputting an MP3 file you can upload to your podcast host, plus the script

Perfect for:
- Creating audio versions of your own blog posts
- Building a podcast feed of your favorite blogs
- Consuming long-form content during your commute

## Why I built this

Sometimes I want to consume interesting articles but don't have time to sit and read. This lets me turn any blog post into something I can listen to while doing chores. The AI voices are nowgood enough that it's actually pleasant to listen to!

## Example usage

```bash
python blogtopod.py 
```

1. In the browswer window that opens, set some values - e.g.

Input URL:  https://example.com/great-article
Output file: great_article.mp3

2. Tap "Run!" to trigger the processing - it might take 6 to 10 minutes.

The app will create `great_article.mp3` and great_article_script.md in your current directory.

## How it works under the hood

The magic happens via:
- [contextkit](https://github.com/AnswerDotAI/contextkit) for page extraction
- Gemini Pro 2.5 for creating a script
- OpenAI latest TTS APIs for high-quality text-to-speech
- Some light audio processing with `pydub` (this current requires a Python version **before** 3.13)

## Making Code Changes

The code is designed to be simple and hackable—feel free to customize the voice and so on. You can edit it using marimo, like so:

`uvx marimo edit --sandbox blogtopod.py`

