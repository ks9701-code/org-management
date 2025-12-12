# MongoDB Atlas Setup Guide - Step by Step

## 🎯 Overview

MongoDB Atlas is MongoDB's cloud database service. The free tier (M0) is perfect for development and this assignment.

## 📋 Step-by-Step Setup

### Step 1: Create MongoDB Atlas Account

1. Go to: **https://www.mongodb.com/cloud/atlas/register**
2. Sign up with:
   - Email address
   - Password
   - Or use Google/GitHub sign-in
3. Verify your email if required

### Step 2: Create a Free Cluster

1. After login, you'll see the **Atlas Dashboard**
2. Click **"Build a Database"** or **"Create"** button
3. Choose **FREE** tier (M0)
4. Select **Cloud Provider & Region**:
   - Choose closest to you (e.g., AWS, US East)
   - Free tier regions are marked
5. Click **"Create"**
6. ⏳ Wait 3-5 minutes for cluster to deploy

### Step 3: Create Database User

1. In the **Security** section, click **"Database Access"**
2. Click **"Add New Database User"**
3. Choose **"Password"** authentication method
4. Enter:
   - **Username**: `admin` (or your choice)
   - **Password**: Click **"Autogenerate Secure Password"** or create your own
   - ⚠️ **SAVE THIS PASSWORD!** You'll need it for the connection string
5. Set **User Privileges**: **"Atlas admin"** (for development)
6. Click **"Add User"**

### Step 4: Configure Network Access (IP Whitelist)

1. In the **Security** section, click **"Network Access"**
2. Click **"Add IP Address"**
3. For **development**, choose one:
   - **Option A (Easier)**: Click **"Allow Access from Anywhere"**
     - This adds `0.0.0.0/0` (all IPs)
     - ⚠️ **Only use with strong password!**
   - **Option B (More Secure)**: Click **"Add Current IP Address"**
     - Adds only your current IP
     - You'll need to update this if your IP changes
4. Click **"Confirm"**

### Step 5: Get Connection String

1. Go back to **"Database"** section (or click **"Connect"** on your cluster)
2. Click **"Connect"** button on your cluster
3. Choose **"Connect your application"**
4. Select:
   - **Driver**: `Python`
   - **Version**: `3.8 or later`
5. Copy the connection string:
   ```
   mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```
6. **Replace `<username>`** with your database user (e.g., `admin`)
7. **Replace `<password>`** with your database user password
8. **Final string should look like:**
   ```
   mongodb+srv://admin:YourPassword123@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```

### Step 6: Test Connection (Optional)

You can test the connection using MongoDB Compass or the MongoDB shell, but for this project, we'll test it when we run the FastAPI app.

## 🔧 Add to Your .env File

Add the connection string to your `.env` file:

```env
MONGO_URI=mongodb+srv://admin:YourPassword123@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
```

**Important:**
- Replace `YourPassword123` with your actual password
- Replace `cluster0.xxxxx` with your actual cluster name
- Keep the entire string on one line
- No spaces around the `=` sign

## ✅ Verification Checklist

- [ ] MongoDB Atlas account created
- [ ] M0 cluster created and deployed
- [ ] Database user created (username + password saved)
- [ ] IP address whitelisted (your IP or 0.0.0.0/0)
- [ ] Connection string copied
- [ ] Connection string updated with username/password
- [ ] Connection string added to `.env` file

## 🐛 Common Issues

### "Authentication failed"
- **Problem**: Wrong username or password in connection string
- **Solution**: Double-check username and password in `.env` file
- Make sure you replaced `<username>` and `<password>` placeholders

### "IP not whitelisted"
- **Problem**: Your IP address is not in the whitelist
- **Solution**: 
  - Go to Network Access in Atlas
  - Add your current IP or use `0.0.0.0/0` for development

### "Connection timeout"
- **Problem**: Network/firewall issue
- **Solution**:
  - Check internet connection
  - Verify IP whitelist includes your IP
  - Try from different network

### "Cluster not found"
- **Problem**: Wrong cluster name in connection string
- **Solution**: Copy connection string again from Atlas dashboard

## 📸 Visual Guide Locations

1. **Cluster Creation**: Dashboard → Build a Database
2. **Database User**: Security → Database Access → Add New User
3. **Network Access**: Security → Network Access → Add IP Address
4. **Connection String**: Database → Connect → Connect your application

## 🚀 Next Steps

After MongoDB Atlas is set up:

1. Create `.env` file with the connection string
2. Run: `python verify_setup.py` to verify everything
3. Start the app: `uvicorn app.main:app --reload --port 8000`
4. Test the API at: http://localhost:8000/docs

## 💡 Pro Tips

- **Save credentials securely**: Use a password manager for database credentials
- **Use environment variables**: Never commit `.env` to git (already in `.gitignore`)
- **Free tier limits**: M0 has 512MB storage - enough for development/testing
- **Cluster name**: You can rename your cluster in Atlas dashboard
- **Monitoring**: Atlas dashboard shows cluster metrics (CPU, storage, etc.)

## 🔒 Security Best Practices

1. **Strong passwords**: Use autogenerated secure passwords
2. **IP whitelisting**: For production, use specific IPs, not `0.0.0.0/0`
3. **Regular updates**: Keep database users updated
4. **Monitor access**: Check Atlas logs for suspicious activity
5. **Backup**: Free tier includes automated backups (limited)

---

**Need help?** Check MongoDB Atlas documentation: https://docs.atlas.mongodb.com/

