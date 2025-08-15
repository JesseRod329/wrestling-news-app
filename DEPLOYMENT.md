# 🚀 Deployment Guide: Real Wrestling News

Deploy your wrestling news app to the cloud for mobile testing and production use.

## 🏆 **Option 1: Render.com (Recommended - Free Tier)**

Render is perfect for Python apps with automatic scaling and free PostgreSQL database.

### Steps:

1. **Create Render Account**: Go to [render.com](https://render.com) and sign up

2. **Connect GitHub**: 
   - Push your code to GitHub repository
   - Connect your GitHub account to Render

3. **Deploy Automatically**:
   - Render will detect the `render.yaml` file and deploy everything automatically
   - Creates both web service and PostgreSQL database
   - Sets up environment variables

4. **Access Your App**:
   - Your app will be available at: `https://wrestling-news-app.onrender.com`
   - Database tables are created automatically on first run

**Pros**: Free tier, automatic deployments, includes database, great for testing
**Cons**: Cold starts on free tier (spins down after 15 min of inactivity)

---

## 🚀 **Option 2: Railway.app (Easy Deploy)**

1. **Create Railway Account**: Go to [railway.app](https://railway.app)

2. **Deploy from GitHub**:
   ```bash
   # Install Railway CLI
   npm install -g @railway/cli
   
   # Login and deploy
   railway login
   railway link
   railway up
   ```

3. **Add PostgreSQL**:
   - In Railway dashboard, click "Add Service" → "PostgreSQL"
   - Railway automatically sets DATABASE_URL environment variable

4. **Set Environment Variables**:
   ```
   ENVIRONMENT=prod
   JWT_SECRET_KEY=your-super-secret-key-here
   ```

**Your app URL**: `https://wrestling-news-app-production.up.railway.app`

---

## 💰 **Option 3: Heroku (Classic Choice)**

1. **Install Heroku CLI**: Download from [heroku.com](https://devcenter.heroku.com/articles/heroku-cli)

2. **Deploy**:
   ```bash
   # Login and create app
   heroku login
   heroku create wrestling-news-app
   
   # Add PostgreSQL addon
   heroku addons:create heroku-postgresql:essential-0
   
   # Set environment variables
   heroku config:set ENVIRONMENT=prod
   heroku config:set JWT_SECRET_KEY=your-super-secret-key-here
   
   # Deploy
   git push heroku main
   ```

**Your app URL**: `https://wrestling-news-app.herokuapp.com`

---

## ⚡ **Option 4: Vercel (Serverless)**

1. **Install Vercel CLI**: `npm install -g vercel`

2. **Deploy**:
   ```bash
   vercel --prod
   ```

3. **Add PostgreSQL**: Use Vercel's PostgreSQL integration or external service like Supabase

---

## 🔧 **Environment Variables Needed**

For any platform, set these environment variables:

```bash
ENVIRONMENT=prod
DATABASE_URL=postgresql://user:password@host:port/dbname  # Auto-set by most platforms
JWT_SECRET_KEY=your-super-secret-key-here-make-it-long-and-random
```

---

## 📱 **Testing from Phone**

Once deployed:

1. **Get your URL** from the deployment platform
2. **Open in mobile browser**: `https://your-app-name.platform.com/static/index.html`
3. **Test all features**:
   - Browse articles with smooth scrolling
   - Test login/register modals
   - Try voting on articles
   - Filter by news sources
   - Search functionality

---

## 🚨 **Troubleshooting**

### Common Issues:

1. **"Internal Server Error"**:
   - Check deployment logs for database connection issues
   - Ensure PostgreSQL database is created and connected

2. **CSS/Images not loading**:
   - Static files should automatically work
   - Check browser console for 404 errors

3. **RSS feeds not working**:
   - Some platforms block outbound HTTP requests
   - Working sources: Wrestling Observer, Pro Wrestling Torch, ESPN, CBS Sports

4. **App is slow**:
   - Free tiers have limitations
   - Consider upgrading to paid tier for better performance

---

## 🎯 **Quick Start - Render (Easiest)**

1. Create account at [render.com](https://render.com)
2. Connect GitHub repo
3. Click "Deploy"
4. Visit your live app!

That's it! Your wrestling news app will be live and accessible from any device. 🎉
