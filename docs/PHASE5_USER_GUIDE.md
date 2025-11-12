# Phase 5 User Guide

Complete guide for using Phase 5 features: real-time notifications, advanced analytics, semantic search, and AI-powered response generation.

## Table of Contents

- [Getting Started](#getting-started)
- [Real-Time Notifications](#real-time-notifications)
- [Advanced Analytics](#advanced-analytics)
- [Semantic Search](#semantic-search)
- [AI Response Generation](#ai-response-generation)
- [Best Practices](#best-practices)
- [FAQ](#faq)

---

## Getting Started

### Accessing the System

1. **Navigate to the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

2. **Login as an agent:**
   - Enter your agent ID (e.g., `agent-123`)
   - System will track your presence and assign you a color

3. **Dashboard Overview:**
   - **Tickets List**: All tickets with real-time updates
   - **Search Bar**: Semantic search across all tickets
   - **Analytics**: Performance metrics and trends
   - **Your Active Tickets**: Tickets you've claimed

---

## Real-Time Notifications

### Understanding Notifications

The system provides instant updates when:
- ✅ New tickets are created
- 👤 Agents claim or release tickets  
- 🔄 Ticket status changes
- 📊 System events occur

### Connection Status

Look for the connection indicator in the top-right corner:
- **🟢 Green**: Connected - receiving real-time updates
- **🟡 Yellow**: Reconnecting...
- **🔴 Red**: Disconnected - click to retry

### Agent Presence

**See who's online:**
- Each agent has a unique color badge
- Active agents shown in sidebar
- Agents who claimed tickets show next to ticket ID

**Your presence:**
- Automatically marked online when connected
- Marked offline after 30 seconds of inactivity
- Presence persists across page refreshes

### Ticket Notifications

**New Ticket Alert:**
```
🎫 New ticket: "Password reset needed"
Priority: P2 | Intent: account_access
[View Ticket]
```

**Ticket Claimed:**
```
👤 Agent Sarah claimed ticket #1234
```

**Ticket Released:**
```
🔓 Ticket #1234 is now available
```

### Managing Notifications

**Desktop Notifications:**
1. Click "Enable Notifications" button
2. Allow browser permission
3. Receive desktop alerts even when tab is inactive

**Notification Settings:**
- Mute notifications for specific ticket types
- Adjust notification sound
- Set "Do Not Disturb" mode

---

## Advanced Analytics

### Analytics Dashboard

**Access:** Click "Analytics" in main navigation

The dashboard provides three main sections:

### 1. Overview Metrics

**Key Metrics:**
- **Total Tickets**: All tickets in selected time period
- **High Priority**: P1 tickets requiring immediate attention
- **Avg Confidence**: Average classification confidence score
- **Low Confidence**: Tickets needing manual review

**Time Range Selector:**
```
[Last 7 Days ▼] [Last 30 Days] [Last 90 Days] [Custom]
```

**Example Insights:**
- 89% of classifications accepted by agents (high accuracy!)
- 12 low-confidence tickets need review
- 87% average confidence score

### 2. Trends Over Time

**Line Charts showing:**
- Daily ticket volume
- High-priority ticket trends
- Resolution rates
- Confidence scores over time

**How to use:**
1. Select time range (7, 14, 30, or 90 days)
2. Hover over points to see exact values
3. Click legend to toggle lines on/off

**What to look for:**
- 📈 Increasing trends: May need more support capacity
- 📉 Decreasing confidence: Check classification quality
- 🔄 Spikes: Identify patterns (weekend drops, product launch surges)

### 3. Distribution Charts

**By Intent:**
```
Billing:           ████████████ 423 tickets (34%)
Technical Issue:   ████████████████ 567 tickets (46%)
Account Access:    ███████ 189 tickets (15%)
General Inquiry:   ██ 68 tickets (5%)
```

**By Sentiment:**
- **Positive** 😊: Happy customers, feedback
- **Neutral** 😐: Standard inquiries
- **Negative** 😞: Issues, complaints (prioritize these!)

**By Priority:**
- **P1** 🔴: Critical (< 1 hour SLA)
- **P2** 🟠: High (< 4 hours SLA)
- **P3** 🟡: Normal (< 24 hours SLA)
- **P4** 🟢: Low (< 48 hours SLA)

### Agent Performance

**Access:** Analytics → Agent Performance tab

**Metrics per agent:**
- **Tickets Claimed**: Total tickets worked on
- **Tickets Resolved**: Successfully closed
- **Resolution Rate**: % of claimed tickets resolved
- **Avg Resolution Time**: Mean time to resolve

**Leaderboard View:**
```
🥇 Sarah Johnson    92.3% resolution rate  |  72 resolved  |  Avg: 1h 12m
🥈 Mike Chen        89.5% resolution rate  |  58 resolved  |  Avg: 1h 45m
🥉 Alex Rivera      87.1% resolution rate  |  45 resolved  |  Avg: 2h 03m
```

**Using Performance Data:**
- Identify top performers for training others
- Spot agents needing support
- Balance workload distribution
- Recognize achievement and improvement

---

## Semantic Search

### How Semantic Search Works

Traditional keyword search finds exact word matches. **Semantic search** understands *meaning*:

**Example:** Searching "login problems"
- ✅ Finds: "can't sign in", "authentication failed", "password not working"
- Traditional search would miss these!

### Search Modes

The system offers **3 search modes**:

#### 1. Semantic Mode (Conceptual)

**Best for:** Finding similar issues regardless of exact wording

**Example:**
```
Search: "billing issues"
Finds:
  - "charged twice this month"
  - "invoice doesn't match my order"
  - "payment method not working"
  - "refund request"
```

**When to use:**
- Exploring related tickets
- Finding patterns across different wordings
- Researching unfamiliar issues

#### 2. Keyword Mode (Exact Match)

**Best for:** Finding specific terms, error codes, or names

**Example:**
```
Search: "ERR_CONNECTION_REFUSED"
Finds only tickets with exact error code
```

**When to use:**
- Looking for specific error messages
- Finding customer by name/ID
- Searching for product names
- Known technical terms

#### 3. Hybrid Mode (Best of Both) ⭐ **Recommended**

**Combines:** 60% semantic + 40% keyword matching

**Example:**
```
Search: "password reset"
Finds:
  - Tickets with exact phrase "password reset"
  - Related: "forgot password", "can't log in", "account access"
```

**When to use:**
- General searches (default mode)
- When you want comprehensive results
- Uncertain of exact terminology

### Using the Search Interface

**1. Enter your search query:**
```
┌──────────────────────────────────────────────┐
│ 🔍 Search tickets...                         │
└──────────────────────────────────────────────┘
```

**2. Select search mode:**
```
( ) Semantic  ( ) Keyword  (•) Hybrid
```

**3. Adjust filters:**
- **Results:** 5, 10, 20, 50
- **Threshold:** Minimum similarity (0.0-1.0)

**4. View results with scores:**
```
🎫 Cannot access my account after password change
   Similarity: 87% | Keyword: 75% | Combined: 83%
   Priority: P2 | Status: Open | 2 hours ago
```

### Search Tips

**✅ DO:**
- Use natural language: "customer can't login"
- Include context: "billing error credit card"
- Try different phrasings if no results
- Use hybrid mode for most searches

**❌ DON'T:**
- Don't use only single words (too broad)
- Don't use complex boolean operators (system handles it)
- Don't worry about spelling (semantic search is fuzzy)

### Advanced Search Techniques

**Find similar to current ticket:**
```
1. View any ticket
2. Click "Find Similar" button
3. System automatically searches using ticket content
```

**Search by specific fields:**
- **By customer:** Include customer ID or name
- **By intent:** Add intent name (billing, technical, etc.)
- **By timeframe:** Use analytics filters then search

**Combining with filters:**
```
Search: "login problems"
+ Filter: High Priority
+ Filter: Last 7 days
+ Filter: Unresolved
```

---

## AI Response Generation

### Overview

The AI assistant helps you draft professional responses using:
- **Similar Tickets**: Past responses that worked
- **Knowledge Base**: Official company documentation  
- **Resolutions**: Proven solutions

### Generating a Response

**Step 1: Open a ticket**
Click on any ticket to view details

**Step 2: Select tone**
```
Tone: [Professional ▼]
      Professional  - Formal, business-appropriate
      Friendly      - Warm and approachable
      Technical     - Detailed with explanations
      Empathetic    - Understanding and supportive
```

**Step 3: Generate**
Click "Generate AI Response" button

**Step 4: Wait for generation** (5-15 seconds)
```
✨ Generating response with llama3.2...
```

**Step 5: Review the response**
```
┌──────────────────────────────────────────────┐
│ Thank you for reaching out about your        │
│ password reset issue. I understand how       │
│ frustrating this can be.                     │
│                                              │
│ To reset your password, please follow these  │
│ steps:                                       │
│ 1. Visit our password reset page at...      │
│ ...                                          │
└──────────────────────────────────────────────┘
```

### Choosing the Right Tone

**Professional** 📋
- Best for: Business customers, formal inquiries
- Example: "Thank you for contacting us. We have reviewed your account..."

**Friendly** 😊
- Best for: Consumer support, positive interactions
- Example: "Hey there! Thanks for reaching out. I'd be happy to help..."

**Technical** 🔧
- Best for: Developers, technical issues, IT support
- Example: "Based on the error code ERR_CONNECTION_REFUSED, this indicates..."

**Empathetic** 💙
- Best for: Complaints, frustrated customers, sensitive issues
- Example: "I'm so sorry you're experiencing this. I completely understand..."

### Editing Generated Responses

**The response is a starting point - always review and customize!**

**1. Edit inline:**
- Click in the response text area
- Make any changes needed
- System tracks that it was edited

**2. Add personal touches:**
- Customer name
- Specific details from their ticket
- Company-specific information

**3. Remove what doesn't apply:**
- Generic placeholders
- Irrelevant suggestions
- Overly formal/informal language

### Saving Responses

**After editing, click "Save Response"**

**What gets saved:**
- ✅ Final response text
- ✅ Tone used
- ✅ Whether you edited it
- ✅ AI model used
- ✅ Timestamp and your agent ID

**Why save?**
- Build a library of successful responses
- Track AI quality improvements
- Reference for similar future tickets
- Training data for new agents

### Viewing Saved Responses

**Scroll to "Saved Response History" section:**

```
💬 Saved Responses (3)

┌─────────────────────────────────────────────────┐
│ Response #1                          [Copy] [⌄] │
│ Tone: Professional | Model: llama3.2            │
│ ✏️ Edited | ✅ Sent | 2 hours ago               │
│                                                  │
│ [Expanded view shows full response text]        │
└─────────────────────────────────────────────────┘
```

**Actions:**
- **Copy**: Copy response to clipboard
- **Expand/Collapse**: View full text
- **Badges**: See tone, edit status, sent status

### Response Quality Tips

**✅ Good responses include:**
- Acknowledge the customer's issue
- Provide clear step-by-step instructions
- Offer alternative solutions
- Include helpful links/resources
- End with offer for further assistance

**Example structure:**
```
1. Greeting + acknowledgment
   "Thank you for contacting us about [issue]."

2. Empathy (if negative sentiment)
   "I understand how frustrating this must be."

3. Solution
   "Here's how to resolve this:
    Step 1: ...
    Step 2: ..."

4. Additional help
   "If this doesn't work, you can also..."

5. Closing
   "Please let me know if you have any questions!"
```

### When NOT to use AI

**Don't use AI for:**
- ❌ Highly sensitive issues (data breaches, legal)
- ❌ Complex multi-step escalations
- ❌ Cases requiring manager approval
- ❌ Responses with financial/refund commitments

**In these cases:**
- Write response manually
- Follow company escalation procedures
- Consult with supervisor

---

## Best Practices

### Daily Workflow

**Morning:**
1. ✅ Check analytics dashboard for overnight tickets
2. ✅ Review high-priority queue
3. ✅ Enable desktop notifications

**During work:**
1. ✅ Claim tickets as you work on them
2. ✅ Use semantic search to find similar resolved tickets
3. ✅ Generate AI responses, then personalize
4. ✅ Monitor real-time notifications for urgent tickets

**End of day:**
1. ✅ Release any uncompleted tickets
2. ✅ Review your performance metrics
3. ✅ Note any recurring issues for team discussion

### Ticket Management

**Claiming tickets:**
- Claim when you start working (not just browsing)
- Only claim tickets you can complete in current session
- Release tickets if interrupted or escalating

**Using AI responses:**
- Generate response early to save time
- Always edit for personalization
- Save successful responses for future reference
- Try different tones if first doesn't fit

**Searching efficiently:**
- Use hybrid mode by default
- Try semantic mode for conceptual exploration
- Use keyword mode for exact error codes
- Check similar tickets before responding

### Team Collaboration

**Stay aware:**
- Watch agent presence to see who's online
- Check claimed tickets to avoid duplicates
- Monitor notifications for team-wide issues

**Share knowledge:**
- Save high-quality AI responses
- Document recurring issues
- Use analytics to identify trends
- Discuss low-confidence tickets in team meetings

---

## FAQ

### General

**Q: Why aren't I seeing real-time updates?**
A: Check the connection indicator (top-right). If red, click to reconnect. Verify your browser supports WebSockets.

**Q: Can I work on multiple tickets at once?**
A: Yes! Claim multiple tickets, but release any you can't complete to free them for teammates.

**Q: What happens if I close the browser?**
A: Your claimed tickets persist. You'll be marked offline after 30 seconds, but tickets remain assigned.

### Search

**Q: Why doesn't keyword search find my ticket?**
A: Try semantic or hybrid mode. Exact word matches may not exist even if the concept does.

**Q: What's a good similarity threshold?**
A: Default (0.3) works for most cases. Increase to 0.6+ for very similar tickets only.

**Q: Can I search by customer name?**
A: Yes! Include name in search query. Hybrid mode works best.

### AI Responses

**Q: How long does AI generation take?**
A: Usually 5-15 seconds. Depends on Ollama server load and model used.

**Q: Why did I get a template response?**
A: Ollama may be unavailable. System provides fallback template. Try again or write manually.

**Q: Is AI response always accurate?**
A: No - ALWAYS review and edit before sending. AI is an assistant, not a replacement.

**Q: Can I regenerate with different tone?**
A: Yes! Change tone dropdown and click "Generate AI Response" again.

**Q: Where do saved responses go?**
A: Saved in database tied to the ticket. View in "Saved Response History" section.

### Analytics

**Q: Why don't my resolved tickets show immediately?**
A: Analytics refresh every few minutes. Check back shortly.

**Q: What's a good resolution rate?**
A: Above 85% is excellent. Below 70% may indicate need for training.

**Q: Can I export analytics data?**
A: Currently view-only. Export feature planned for future release.

### Performance

**Q: System feels slow. What to do?**
A: Check your internet connection. Clear browser cache. Contact IT if persistent.

**Q: AI generation timeout?**
A: Ollama may be overloaded. Try again in a minute. Use fallback template if urgent.

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl/Cmd + K` | Focus search bar |
| `Ctrl/Cmd + N` | View notifications |
| `Ctrl/Cmd + A` | Open analytics |
| `Esc` | Close modals |
| `G` then `R` | Generate AI response (on ticket view) |
| `S` | Save current response |

---

## Getting Help

**Technical Issues:**
- Check [Deployment Guide](./PHASE5_DEPLOYMENT.md) for system status
- View [API Documentation](./PHASE5_API_DOCS.md) for endpoints
- Contact IT support: support@company.com

**Feature Requests:**
- Submit via feedback form
- Join weekly product meetings
- Contribute to internal wiki

**Training:**
- New agent onboarding: Weekly Wednesdays
- Advanced features: Monthly workshops
- 1-on-1 coaching: Schedule with team lead

---

## Appendix: Response Templates

### Quick Response Templates

**Password Reset:**
```
Thank you for reaching out about your password reset issue.

To reset your password:
1. Visit [company-url]/reset
2. Enter your email address
3. Check your inbox for reset link (check spam folder)
4. Click link and create new password

If you don't receive the email within 5 minutes, please reply and I'll assist further.
```

**Billing Inquiry:**
```
I'd be happy to help with your billing question.

[Acknowledge specific issue]

[Provide explanation or solution]

If you have any other questions about your bill, please don't hesitate to ask!
```

**Technical Issue:**
```
I understand you're experiencing [specific issue]. Let me help troubleshoot this.

Can you please provide:
- Error message (if any)
- Browser/device you're using
- When the issue started

In the meantime, you can try:
1. [First troubleshooting step]
2. [Second troubleshooting step]

I'll investigate further and get back to you shortly.
```

---

**Happy supporting! 🎉**
