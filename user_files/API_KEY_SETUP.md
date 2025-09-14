# OpenAI API Key Configuration

## Quick Setup

### Option 1: Through AnkiBrain Menu (Recommended)
1. Start Anki with AnkiBrain installed
2. Go to **Tools** → **AnkiBrain** → **Set OpenAI API Key...**
3. Enter your OpenAI API key in the dialog
4. Click **Save**

### Option 2: Manual Configuration
1. Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)
2. Edit the file `user_files/.env` in your AnkiBrain installation
3. Replace `your-api-key-here` with your actual API key:
   ```
   OPENAI_API_KEY=sk-your-actual-api-key-here
   ```
4. Restart Anki

## Supported Models
AnkiBrain now supports all latest OpenAI models:
- **gpt-3.5-turbo** (default, most economical)
- **gpt-4** (expensive, high quality)
- **gpt-4o** (advanced reasoning)
- **gpt-4o-mini** (efficient, good balance)
- **gpt-5** (premium, latest model)
- **gpt-5-mini** (fast, good quality)
- **gpt-5-nano** (ultra-fast, basic tasks)

## Troubleshooting
- **"Error making cards"**: Usually means API key is not configured or invalid
- **Models not appearing**: Restart Anki after configuring API key
- **API errors**: Check your OpenAI account has sufficient credits

## API Key Security
- Never share your API key publicly
- Keep your API key private and secure
- Monitor your OpenAI usage and billing