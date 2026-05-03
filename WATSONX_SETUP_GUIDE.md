# IBM watsonx.ai Setup Guide

This guide will walk you through getting your IBM watsonx.ai API credentials step-by-step.

## Prerequisites

- An IBM Cloud account (free tier available)
- Access to IBM watsonx.ai service

---

## Step 1: Create an IBM Cloud Account

1. **Visit IBM Cloud**: Go to [https://cloud.ibm.com/registration](https://cloud.ibm.com/registration)

2. **Sign up for free**:
   - Enter your email address
   - Create a password
   - Verify your email
   - Complete the registration form

3. **Choose the Lite (Free) plan** - No credit card required for basic usage

---

## Step 2: Access watsonx.ai

1. **Log in to IBM Cloud**: [https://cloud.ibm.com/](https://cloud.ibm.com/)

2. **Navigate to watsonx.ai**:
   - Click on the **Catalog** in the top menu
   - Search for "watsonx.ai" or find it under **AI / Machine Learning**
   - Click on **watsonx.ai**

3. **Create the service**:
   - Select your region (e.g., Dallas, Frankfurt, Tokyo)
   - Choose a pricing plan (Lite plan is free)
   - Click **Create**

---

## Step 3: Create a watsonx.ai Project

1. **Go to watsonx.ai dashboard**:
   - From IBM Cloud dashboard, click on **Resource list**
   - Find and click on your **watsonx.ai** service
   - Click **Launch watsonx.ai**

2. **Create a new project**:
   - Click **Projects** in the left sidebar
   - Click **New project**
   - Choose **Create an empty project**
   - Enter a project name (e.g., "Bob DevOps Control Tower")
   - Add a description (optional)
   - Click **Create**

3. **Get your Project ID**:
   - Open your project
   - Click on the **Manage** tab
   - Find **Project ID** under General
   - **Copy this ID** - you'll need it for `WATSONX_PROJECT_ID`

---

## Step 4: Generate an API Key

1. **Go to IBM Cloud IAM**:
   - Visit [https://cloud.ibm.com/iam/apikeys](https://cloud.ibm.com/iam/apikeys)
   - Or: Click your profile icon → **Manage** → **Access (IAM)** → **API keys**

2. **Create a new API key**:
   - Click **Create** button (or **Create an IBM Cloud API key**)
   - Enter a name (e.g., "watsonx-devops-tower")
   - Add a description (optional)
   - Click **Create**

3. **Save your API key**:
   - **IMPORTANT**: Copy the API key immediately
   - Click **Download** to save it as a file (recommended)
   - You won't be able to see it again!
   - This is your `WATSONX_API_KEY`

---

## Step 5: Configure Your Project

1. **Copy the example config**:
   ```bash
   cp config.example.env .env
   ```

2. **Edit the .env file** with your credentials:
   ```env
   # Replace with your actual API key from Step 4
   WATSONX_API_KEY=your_actual_api_key_here
   
   # Replace with your Project ID from Step 3
   WATSONX_PROJECT_ID=your_actual_project_id_here
   
   # Default URL (change if using different region)
   WATSONX_URL=https://us-south.ml.cloud.ibm.com
   
   # Model settings (these defaults work well)
   WATSONX_MODEL_ID=ibm/granite-13b-chat-v2
   WATSONX_MAX_TOKENS=500
   WATSONX_TEMPERATURE=0.7
   ```

3. **Save the file**

---

## Step 6: Verify Your Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Test the integration**:
   ```bash
   python -m app.main --repo ./demo_repo
   ```

3. **Check the output**:
   - If configured correctly, you'll see AI-generated summaries
   - If there's an issue, you'll see a fallback summary with a warning

---

## Regional Endpoints

Choose the appropriate URL based on your watsonx.ai service region:

| Region | URL |
|--------|-----|
| **US South (Dallas)** | `https://us-south.ml.cloud.ibm.com` |
| **EU (Frankfurt)** | `https://eu-de.ml.cloud.ibm.com` |
| **EU (London)** | `https://eu-gb.ml.cloud.ibm.com` |
| **Asia Pacific (Tokyo)** | `https://jp-tok.ml.cloud.ibm.com` |

---

## Available Models

You can use different models by changing `WATSONX_MODEL_ID`:

### Recommended Models:

- **ibm/granite-13b-chat-v2** (Default) - Best for general tasks
- **ibm/granite-20b-multilingual** - For multilingual support
- **meta-llama/llama-3-70b-instruct** - More powerful, higher cost
- **mistralai/mixtral-8x7b-instruct-v01** - Good balance of speed/quality

---

## Troubleshooting

### "WATSONX_API_KEY environment variable is required"

**Solution**: Make sure your `.env` file exists and contains valid credentials.

### "Invalid API key"

**Solutions**:
1. Verify you copied the entire API key (no spaces)
2. Check if the API key is still active in IBM Cloud
3. Generate a new API key if needed

### "Project not found"

**Solutions**:
1. Verify the Project ID is correct
2. Ensure the project exists in your watsonx.ai account
3. Check that your API key has access to the project

### "Region mismatch"

**Solution**: Make sure `WATSONX_URL` matches the region where you created your watsonx.ai service.

### "Rate limit exceeded"

**Solution**: 
- Free tier has usage limits
- Wait a few minutes and try again
- Consider upgrading to a paid plan for higher limits

---

## Cost Information

### Free Tier (Lite Plan):
- ✅ No credit card required
- ✅ Limited API calls per month
- ✅ Access to select models
- ✅ Perfect for testing and development

### Paid Plans:
- Pay-as-you-go pricing
- Higher rate limits
- Access to all models
- Production-ready

**Pricing**: Check current rates at [https://www.ibm.com/products/watsonx-ai/pricing](https://www.ibm.com/products/watsonx-ai/pricing)

---

## Security Best Practices

1. ✅ **Never commit .env files** to version control
2. ✅ **Rotate API keys regularly** (every 90 days recommended)
3. ✅ **Use separate keys** for development and production
4. ✅ **Restrict API key permissions** to only what's needed
5. ✅ **Monitor usage** in IBM Cloud dashboard

---

## Quick Reference

### Where to find things:

| Item | Location |
|------|----------|
| **API Keys** | [cloud.ibm.com/iam/apikeys](https://cloud.ibm.com/iam/apikeys) |
| **watsonx.ai Dashboard** | [dataplatform.cloud.ibm.com/wx](https://dataplatform.cloud.ibm.com/wx) |
| **Project ID** | watsonx.ai → Projects → Your Project → Manage tab |
| **Usage/Billing** | [cloud.ibm.com/billing](https://cloud.ibm.com/billing) |
| **Documentation** | [ibm.com/docs/watsonx](https://www.ibm.com/docs/watsonx) |

---

## Need Help?

- **IBM watsonx.ai Documentation**: [https://www.ibm.com/docs/watsonx](https://www.ibm.com/docs/watsonx)
- **IBM Cloud Support**: [https://cloud.ibm.com/unifiedsupport/supportcenter](https://cloud.ibm.com/unifiedsupport/supportcenter)
- **Community Forums**: [https://community.ibm.com/community/user/watsonx/home](https://community.ibm.com/community/user/watsonx/home)

---

## Summary Checklist

- [ ] Created IBM Cloud account
- [ ] Created watsonx.ai service
- [ ] Created a watsonx.ai project
- [ ] Copied Project ID
- [ ] Generated API key
- [ ] Created .env file with credentials
- [ ] Installed Python dependencies
- [ ] Tested the integration
- [ ] Verified AI summaries are working

Once all items are checked, you're ready to use watsonx.ai with Bob DevOps Control Tower! 🚀