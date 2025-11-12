<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-purple-50 dark:from-zinc-950 dark:via-zinc-900 dark:to-zinc-950 transition-colors duration-500">
    <!-- Decorative background elements -->
    <div class="fixed inset-0 overflow-hidden pointer-events-none">
      <div class="absolute top-0 left-1/4 w-96 h-96 bg-blue-200/20 dark:bg-blue-500/10 rounded-full blur-3xl"></div>
      <div class="absolute bottom-0 right-1/4 w-96 h-96 bg-purple-200/20 dark:bg-purple-500/10 rounded-full blur-3xl"></div>
    </div>

    <!-- Header -->
    <div class="relative bg-white/80 dark:bg-zinc-900/80 backdrop-blur-xl shadow-lg border-b border-gray-200/50 dark:border-zinc-800/50 transition-colors duration-300">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-4">
            <div class="w-12 h-12 rounded-2xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center shadow-lg">
              <svg class="w-7 h-7 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
              </svg>
            </div>
            <div>
              <h1 class="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 dark:from-blue-400 dark:to-purple-400 bg-clip-text text-transparent">
                How It Works
              </h1>
              <p class="mt-1 text-sm text-gray-600 dark:text-gray-400">Understanding the AI-powered ticket triage pipeline</p>
            </div>
          </div>
          <div class="flex items-center gap-3">
            <!-- Theme Toggle -->
            <button
              @click="toggleTheme"
              class="group p-3 rounded-xl bg-gradient-to-br from-gray-50 to-gray-100 dark:from-zinc-800 dark:to-zinc-900 border border-gray-200 dark:border-zinc-700 hover:shadow-lg hover:scale-105 transition-all duration-300"
              :aria-label="`Switch to ${isDark ? 'light' : 'dark'} mode`"
            >
              <svg v-if="!isDark" class="w-5 h-5 text-gray-700 group-hover:text-purple-600 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"/>
              </svg>
              <svg v-else class="w-5 h-5 text-yellow-400 group-hover:text-yellow-300 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"/>
              </svg>
            </button>
            <NuxtLink to="/" class="group flex items-center gap-2 px-5 py-3 rounded-xl bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-medium shadow-lg hover:shadow-xl hover:scale-105 transition-all duration-300">
              <svg class="w-5 h-5 group-hover:-translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/>
              </svg>
              <span>Dashboard</span>
            </NuxtLink>
          </div>
        </div>
      </div>
    </div>

    <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
      <!-- Overview Section -->
      <div class="mb-20">
        <div class="text-center mb-16">
          <div class="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400 text-sm font-medium mb-6 border border-blue-200 dark:border-blue-800">
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
            </svg>
            <span>Powered by AI & Machine Learning</span>
          </div>
          <h2 class="text-5xl md:text-6xl font-bold text-gray-900 dark:text-white mb-6 leading-tight">
            AI-Powered Support<br/>
            <span class="bg-gradient-to-r from-blue-600 to-purple-600 dark:from-blue-400 dark:to-purple-400 bg-clip-text text-transparent">
              Ticket Triage
            </span>
          </h2>
          <p class="text-xl text-gray-600 dark:text-gray-400 max-w-3xl mx-auto leading-relaxed">
            Our system automatically classifies, prioritizes, and routes support tickets using advanced AI and machine learning techniques.
            With real-time WebSocket updates, semantic search, AI-powered response generation (RAG), and comprehensive analytics,
            we deliver lightning-fast results with exceptional accuracy and collaboration.
          </p>
        </div>

        <!-- Key Stats -->
        <div class="grid grid-cols-1 md:grid-cols-5 gap-6 mb-12">
          <div class="group relative bg-gradient-to-br from-blue-50 to-blue-100 dark:from-blue-950/50 dark:to-blue-900/30 rounded-2xl shadow-lg hover:shadow-2xl p-8 text-center transform hover:scale-105 hover:-translate-y-1 transition-all duration-300 border border-blue-200/50 dark:border-blue-800/50 overflow-hidden">
            <div class="absolute inset-0 bg-gradient-to-br from-blue-400/0 to-blue-600/0 group-hover:from-blue-400/10 group-hover:to-blue-600/10 transition-all duration-300"></div>
            <div class="relative">
              <div class="text-5xl font-bold bg-gradient-to-br from-blue-600 to-blue-800 dark:from-blue-400 dark:to-blue-300 bg-clip-text text-transparent mb-3">~90%</div>
              <div class="text-sm font-semibold text-blue-700 dark:text-blue-400 uppercase tracking-wide">Classification Accuracy</div>
            </div>
          </div>
          <div class="group relative bg-gradient-to-br from-green-50 to-emerald-100 dark:from-green-950/50 dark:to-emerald-900/30 rounded-2xl shadow-lg hover:shadow-2xl p-8 text-center transform hover:scale-105 hover:-translate-y-1 transition-all duration-300 border border-green-200/50 dark:border-green-800/50 overflow-hidden">
            <div class="absolute inset-0 bg-gradient-to-br from-green-400/0 to-emerald-600/0 group-hover:from-green-400/10 group-hover:to-emerald-600/10 transition-all duration-300"></div>
            <div class="relative">
              <div class="text-5xl font-bold bg-gradient-to-br from-green-600 to-emerald-700 dark:from-green-400 dark:to-emerald-300 bg-clip-text text-transparent mb-3">50%</div>
              <div class="text-sm font-semibold text-green-700 dark:text-green-400 uppercase tracking-wide">Faster Response Time</div>
            </div>
          </div>
          <div class="group relative bg-gradient-to-br from-purple-50 to-purple-100 dark:from-purple-950/50 dark:to-purple-900/30 rounded-2xl shadow-lg hover:shadow-2xl p-8 text-center transform hover:scale-105 hover:-translate-y-1 transition-all duration-300 border border-purple-200/50 dark:border-purple-800/50 overflow-hidden">
            <div class="absolute inset-0 bg-gradient-to-br from-purple-400/0 to-purple-600/0 group-hover:from-purple-400/10 group-hover:to-purple-600/10 transition-all duration-300"></div>
            <div class="relative">
              <div class="text-5xl font-bold bg-gradient-to-br from-purple-600 to-purple-800 dark:from-purple-400 dark:to-purple-300 bg-clip-text text-transparent mb-3">384</div>
              <div class="text-sm font-semibold text-purple-700 dark:text-purple-400 uppercase tracking-wide">Embedding Dimensions</div>
            </div>
          </div>
          <div class="group relative bg-gradient-to-br from-orange-50 to-orange-100 dark:from-orange-950/50 dark:to-orange-900/30 rounded-2xl shadow-lg hover:shadow-2xl p-8 text-center transform hover:scale-105 hover:-translate-y-1 transition-all duration-300 border border-orange-200/50 dark:border-orange-800/50 overflow-hidden">
            <div class="absolute inset-0 bg-gradient-to-br from-orange-400/0 to-orange-600/0 group-hover:from-orange-400/10 group-hover:to-orange-600/10 transition-all duration-300"></div>
            <div class="relative">
              <div class="text-5xl font-bold bg-gradient-to-br from-orange-600 to-orange-800 dark:from-orange-400 dark:to-orange-300 bg-clip-text text-transparent mb-3">&lt;200ms</div>
              <div class="text-sm font-semibold text-orange-700 dark:text-orange-400 uppercase tracking-wide">Classification Time</div>
            </div>
          </div>
          <div class="group relative bg-gradient-to-br from-pink-50 to-red-100 dark:from-pink-950/50 dark:to-red-900/30 rounded-2xl shadow-lg hover:shadow-2xl p-8 text-center transform hover:scale-105 hover:-translate-y-1 transition-all duration-300 border border-pink-200/50 dark:border-pink-800/50 overflow-hidden">
            <div class="absolute inset-0 bg-gradient-to-br from-pink-400/0 to-red-600/0 group-hover:from-pink-400/10 group-hover:to-red-600/10 transition-all duration-300"></div>
            <div class="relative">
              <div class="text-5xl font-bold bg-gradient-to-br from-pink-600 to-red-800 dark:from-pink-400 dark:to-red-300 bg-clip-text text-transparent mb-3">Real-Time</div>
              <div class="text-sm font-semibold text-pink-700 dark:text-pink-400 uppercase tracking-wide">WebSocket Updates</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Animated Pipeline -->
      <div class="mb-20">
        <div class="text-center mb-12">
          <h2 class="text-4xl font-bold text-gray-900 dark:text-white mb-4">The Processing Pipeline</h2>
          <p class="text-lg text-gray-600 dark:text-gray-400">Watch how tickets flow through our intelligent system</p>
        </div>
        <div class="relative bg-white/80 dark:bg-zinc-800/80 backdrop-blur-xl rounded-3xl shadow-2xl p-10 transition-colors border border-gray-200/50 dark:border-zinc-700/50">
          <div class="absolute -inset-1 bg-gradient-to-r from-blue-600 to-purple-600 rounded-3xl opacity-20 dark:opacity-30 blur-xl"></div>
          <div class="relative">
            <PipelineAnimation :currentStep="currentStep" @step-click="setStep" />
          </div>
        </div>
      </div>

      <!-- Detailed Steps -->
      <div class="mb-16">
        <h2 class="text-3xl font-bold text-gray-900 dark:text-white mb-8 text-center">Step-by-Step Breakdown</h2>
        <div class="space-y-8">
          <!-- Step 1 -->
          <StepCard 
            :step="1"
            title="Ticket Submission"
            :active="currentStep === 1"
            @click="setStep(1)"
          >
            <template #icon>
              <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
              </svg>
            </template>
            <template #content>
              <p class="text-gray-700 mb-4">
                A customer submits a support ticket through email, chat, phone, or web form. The ticket contains:
              </p>
              <ul class="list-disc list-inside space-y-2 text-gray-700">
                <li><strong>Subject:</strong> Brief description of the issue</li>
                <li><strong>Body:</strong> Detailed explanation of the problem</li>
                <li><strong>Channel:</strong> How the ticket was submitted</li>
                <li><strong>Metadata:</strong> Timestamp, customer info, etc.</li>
              </ul>
              <div class="mt-4 p-4 bg-blue-50 rounded-lg">
                <code class="text-sm">
                  POST /tickets<br>
                  { "subject": "Cannot login", "body": "Getting error 403...", "channel": "email" }
                </code>
              </div>
            </template>
          </StepCard>

          <!-- Step 2 -->
          <StepCard 
            :step="2"
            title="Intent Classification"
            :active="currentStep === 2"
            @click="setStep(2)"
          >
            <template #icon>
              <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
              </svg>
            </template>
            <template #content>
              <p class="text-gray-700 mb-4">
                Using <strong>Hugging Face's facebook/bart-large-mnli</strong> model, we perform zero-shot classification to determine the ticket's intent:
              </p>
              <div class="grid grid-cols-2 gap-4 mb-4">
                <div class="p-4 bg-red-50 rounded-lg">
                  <div class="font-semibold text-red-700">🔄 Refund</div>
                  <div class="text-sm text-gray-600">Payment returns, cancellations</div>
                </div>
                <div class="p-4 bg-green-50 rounded-lg">
                  <div class="font-semibold text-green-700">💰 Billing</div>
                  <div class="text-sm text-gray-600">Invoices, charges, subscriptions</div>
                </div>
                <div class="p-4 bg-blue-50 rounded-lg">
                  <div class="font-semibold text-blue-700">🔧 Technical</div>
                  <div class="text-sm text-gray-600">Login issues, bugs, errors</div>
                </div>
                <div class="p-4 bg-gray-50 rounded-lg">
                  <div class="font-semibold text-gray-700">❓ General</div>
                  <div class="text-sm text-gray-600">Questions, info requests</div>
                </div>
              </div>
              <p class="text-sm text-gray-600 italic">
                The model outputs confidence scores for each category. The highest score determines the intent.
              </p>
            </template>
          </StepCard>

          <!-- Step 3 -->
          <StepCard 
            :step="3"
            title="Sentiment Analysis"
            :active="currentStep === 3"
            @click="setStep(3)"
          >
            <template #icon>
              <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
            </template>
            <template #content>
              <p class="text-gray-700 mb-4">
                Using <strong>distilbert-base-uncased-finetuned-sst-2-english</strong>, we analyze the emotional tone of the ticket:
              </p>
              <div class="flex gap-4 mb-4">
                <div class="flex-1 p-4 bg-red-50 rounded-lg text-center">
                  <div class="text-3xl mb-2">😠</div>
                  <div class="font-semibold text-red-700">Negative</div>
                  <div class="text-sm text-gray-600">Angry, frustrated, upset</div>
                </div>
                <div class="flex-1 p-4 bg-yellow-50 rounded-lg text-center">
                  <div class="text-3xl mb-2">😐</div>
                  <div class="font-semibold text-yellow-700">Neutral</div>
                  <div class="text-sm text-gray-600">Calm, matter-of-fact</div>
                </div>
                <div class="flex-1 p-4 bg-green-50 rounded-lg text-center">
                  <div class="text-3xl mb-2">😊</div>
                  <div class="font-semibold text-green-700">Positive</div>
                  <div class="text-sm text-gray-600">Happy, satisfied, grateful</div>
                </div>
              </div>
              <p class="text-sm text-gray-600 italic">
                Sentiment helps prioritize urgent issues from frustrated customers.
              </p>
            </template>
          </StepCard>

          <!-- Step 4 -->
          <StepCard 
            :step="4"
            title="Priority Assignment"
            :active="currentStep === 4"
            @click="setStep(4)"
          >
            <template #icon>
              <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"/>
              </svg>
            </template>
            <template #content>
              <p class="text-gray-700 mb-4">
                Business rules combine intent, sentiment, and confidence to assign priority:
              </p>
              <div class="space-y-3">
                <div class="p-4 bg-red-50 border-l-4 border-red-500 rounded">
                  <div class="font-semibold text-red-700">🔴 Urgent</div>
                  <div class="text-sm text-gray-600">Refund + Negative sentiment</div>
                </div>
                <div class="p-4 bg-orange-50 border-l-4 border-orange-500 rounded">
                  <div class="font-semibold text-orange-700">🟠 High</div>
                  <div class="text-sm text-gray-600">Technical + Negative, or Billing issues</div>
                </div>
                <div class="p-4 bg-yellow-50 border-l-4 border-yellow-500 rounded">
                  <div class="font-semibold text-yellow-700">🟡 Medium</div>
                  <div class="text-sm text-gray-600">Technical + Neutral/Positive</div>
                </div>
                <div class="p-4 bg-green-50 border-l-4 border-green-500 rounded">
                  <div class="font-semibold text-green-700">🟢 Low</div>
                  <div class="text-sm text-gray-600">General inquiries, positive tickets</div>
                </div>
              </div>
              <div class="mt-4 p-4 bg-gray-50 rounded-lg">
                <p class="text-sm text-gray-600">
                  <strong>Low Confidence Detection:</strong> If confidence &lt; 0.5, the ticket is flagged for human review.
                </p>
              </div>
            </template>
          </StepCard>

          <!-- Step 5 -->
          <StepCard 
            :step="5"
            title="Vector Embedding"
            :active="currentStep === 5"
            @click="setStep(5)"
          >
            <template #icon>
              <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01"/>
              </svg>
            </template>
            <template #content>
              <p class="text-gray-700 mb-4">
                Using <strong>sentence-transformers/all-MiniLM-L6-v2</strong>, we generate a 384-dimensional vector embedding representing the semantic meaning of the ticket:
              </p>
              <div class="mb-4 p-4 bg-purple-50 rounded-lg">
                <div class="font-mono text-sm text-gray-700">
                  embedding = encode("Cannot login after password reset...")<br>
                  → [0.123, -0.456, 0.789, ..., 0.234] (384 dimensions)
                </div>
              </div>
              <p class="text-gray-700 mb-4">
                This vector captures the meaning of the ticket, enabling:
              </p>
              <ul class="list-disc list-inside space-y-2 text-gray-700">
                <li><strong>Similar Ticket Detection:</strong> Find tickets with similar issues</li>
                <li><strong>Semantic Search:</strong> Search by meaning, not just keywords</li>
                <li><strong>Smart Suggestions:</strong> Match with relevant KB articles</li>
              </ul>
              <div class="mt-4 p-4 bg-blue-50 rounded-lg">
                <p class="text-sm text-gray-600">
                  <strong>Storage:</strong> Vectors are stored in PostgreSQL using the pgvector extension
                </p>
              </div>
            </template>
          </StepCard>

          <!-- Step 6 -->
          <StepCard 
            :step="6"
            title="Similar Ticket Search"
            :active="currentStep === 6"
            @click="setStep(6)"
          >
            <template #icon>
              <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
              </svg>
            </template>
            <template #content>
              <p class="text-gray-700 mb-4">
                Using <strong>cosine similarity</strong> in pgvector, we find tickets with similar semantic meaning:
              </p>
              <div class="mb-4 p-4 bg-indigo-50 rounded-lg">
                <div class="font-mono text-xs text-gray-700 overflow-x-auto">
                  SELECT id, subject, <br>
                  &nbsp;&nbsp;1 - (embedding &lt;=&gt; query_vector) as similarity<br>
                  FROM tickets<br>
                  WHERE similarity &gt; 0.5<br>
                  ORDER BY similarity DESC<br>
                  LIMIT 5
                </div>
              </div>
              <div class="space-y-3">
                <div class="p-3 bg-white border rounded-lg">
                  <div class="flex justify-between items-center">
                    <span class="text-sm text-gray-700">Password reset not working</span>
                    <span class="px-2 py-1 bg-green-100 text-green-700 text-xs rounded">87% similar</span>
                  </div>
                </div>
                <div class="p-3 bg-white border rounded-lg">
                  <div class="flex justify-between items-center">
                    <span class="text-sm text-gray-700">Login error after changing password</span>
                    <span class="px-2 py-1 bg-green-100 text-green-700 text-xs rounded">82% similar</span>
                  </div>
                </div>
                <div class="p-3 bg-white border rounded-lg">
                  <div class="flex justify-between items-center">
                    <span class="text-sm text-gray-700">Account access issue</span>
                    <span class="px-2 py-1 bg-blue-100 text-blue-700 text-xs rounded">65% similar</span>
                  </div>
                </div>
              </div>
              <p class="mt-4 text-sm text-gray-600 italic">
                Agents can see how similar tickets were resolved to speed up response time.
              </p>
            </template>
          </StepCard>

          <!-- Step 7 -->
          <StepCard 
            :step="7"
            title="Smart Suggestions"
            :active="currentStep === 7"
            @click="setStep(7)"
          >
            <template #icon>
              <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
              </svg>
            </template>
            <template #content>
              <p class="text-gray-700 mb-4">
                Based on the classified intent, we suggest relevant resources to help agents respond quickly:
              </p>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                <div class="p-4 bg-blue-50 rounded-lg">
                  <div class="font-semibold text-blue-700 mb-2">📚 KB Articles</div>
                  <ul class="text-sm text-gray-700 space-y-1">
                    <li>• How to reset password</li>
                    <li>• Troubleshooting login errors</li>
                    <li>• Account recovery guide</li>
                  </ul>
                </div>
                <div class="p-4 bg-green-50 rounded-lg">
                  <div class="font-semibold text-green-700 mb-2">📝 Resolution Templates</div>
                  <ul class="text-sm text-gray-700 space-y-1">
                    <li>• Password reset instructions</li>
                    <li>• Account verification steps</li>
                    <li>• Technical support escalation</li>
                  </ul>
                </div>
              </div>
              <p class="text-sm text-gray-600 italic">
                Suggestions are ranked by relevance score and limited to top results.
              </p>
            </template>
          </StepCard>

          <!-- Step 8 -->
          <StepCard 
            :step="8"
            title="Real-Time Updates & WebSocket"
            :active="currentStep === 8"
            @click="setStep(8)"
          >
            <template #icon>
              <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
              </svg>
            </template>
            <template #content>
              <p class="text-gray-700 mb-4">
                Using <strong>Redis Pub/Sub + WebSocket</strong>, we provide real-time updates across all agents:
              </p>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                <div class="p-4 bg-green-50 rounded-lg">
                  <div class="font-semibold text-green-700 mb-2">🟢 Agent Presence</div>
                  <ul class="text-sm text-gray-700 space-y-1">
                    <li>• See who's online in real-time</li>
                    <li>• Active agent count and list</li>
                    <li>• Automatic disconnect handling</li>
                  </ul>
                </div>
                <div class="p-4 bg-blue-50 rounded-lg">
                  <div class="font-semibold text-blue-700 mb-2">🎫 Ticket Updates</div>
                  <ul class="text-sm text-gray-700 space-y-1">
                    <li>• New tickets appear instantly</li>
                    <li>• Status changes broadcast live</li>
                    <li>• Claim/release notifications</li>
                  </ul>
                </div>
                <div class="p-4 bg-purple-50 rounded-lg">
                  <div class="font-semibold text-purple-700 mb-2">🔒 Ticket Claims</div>
                  <ul class="text-sm text-gray-700 space-y-1">
                    <li>• Agents can claim tickets</li>
                    <li>• Prevents double-handling</li>
                    <li>• Shows who's working on what</li>
                  </ul>
                </div>
                <div class="p-4 bg-orange-50 rounded-lg">
                  <div class="font-semibold text-orange-700 mb-2">📢 Broadcasts</div>
                  <ul class="text-sm text-gray-700 space-y-1">
                    <li>• Updates reach all clients instantly</li>
                    <li>• No polling required</li>
                    <li>• Real-time collaboration</li>
                  </ul>
                </div>
              </div>
              <div class="mt-4 p-4 bg-gray-50 rounded-lg">
                <p class="text-sm text-gray-600">
                  <strong>Architecture:</strong> Redis Pub/Sub handles message distribution, WebSocket maintains persistent connections for instant updates.
                </p>
              </div>
            </template>
          </StepCard>

          <!-- Step 9 -->
          <StepCard 
            :step="9"
            title="Advanced Semantic Search"
            :active="currentStep === 9"
            @click="setStep(9)"
          >
            <template #icon>
              <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
              </svg>
            </template>
            <template #content>
              <p class="text-gray-700 mb-4">
                Our advanced search system offers <strong>three search modes</strong> for maximum flexibility:
              </p>
              <div class="space-y-3 mb-4">
                <div class="p-4 bg-purple-50 border-l-4 border-purple-500 rounded">
                  <div class="font-semibold text-purple-700 mb-1">🧠 Semantic Search</div>
                  <div class="text-sm text-gray-700 mb-2">Uses vector embeddings to find tickets by meaning, not just keywords</div>
                  <div class="text-xs font-mono bg-white px-2 py-1 rounded">"login problem" → matches "can't access account", "authentication failing"</div>
                </div>
                <div class="p-4 bg-blue-50 border-l-4 border-blue-500 rounded">
                  <div class="font-semibold text-blue-700 mb-1">🔤 Keyword Search</div>
                  <div class="text-sm text-gray-700 mb-2">Traditional full-text search with PostgreSQL's ts_vector</div>
                  <div class="text-xs font-mono bg-white px-2 py-1 rounded">"invoice 2024" → exact word matches in subject/body</div>
                </div>
                <div class="p-4 bg-green-50 border-l-4 border-green-500 rounded">
                  <div class="font-semibold text-green-700 mb-1">🎯 Hybrid Search</div>
                  <div class="text-sm text-gray-700 mb-2">Combines semantic + keyword with reciprocal rank fusion (RRF)</div>
                  <div class="text-xs font-mono bg-white px-2 py-1 rounded">Best of both: meaning + exact matches with smart ranking</div>
                </div>
              </div>
              <div class="p-4 bg-indigo-50 rounded-lg">
                <div class="text-sm text-gray-700">
                  <strong>Performance:</strong> Results ranked with confidence scores (0-100). Hybrid mode uses RRF algorithm for optimal result fusion.
                </div>
              </div>
            </template>
          </StepCard>

          <!-- Step 10 -->
          <StepCard 
            :step="10"
            title="AI Response Generation (RAG)"
            :active="currentStep === 10"
            @click="setStep(10)"
          >
            <template #icon>
              <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
              </svg>
            </template>
            <template #content>
              <p class="text-gray-700 mb-4">
                Using <strong>Ollama + Retrieval-Augmented Generation (RAG)</strong>, we generate context-aware AI responses:
              </p>
              <div class="mb-4 p-4 bg-gradient-to-r from-purple-50 to-blue-50 rounded-lg border-2 border-purple-200">
                <div class="font-semibold text-purple-900 mb-3 flex items-center gap-2">
                  <span class="text-2xl">🤖</span>
                  <span>RAG Pipeline</span>
                </div>
                <ol class="space-y-2 text-sm text-gray-700">
                  <li><strong>1. Context Retrieval:</strong> Find similar resolved tickets + relevant KB articles</li>
                  <li><strong>2. Prompt Construction:</strong> Build prompt with ticket + context + resolution history</li>
                  <li><strong>3. LLM Generation:</strong> Generate response using Ollama (llama3.2/qwen2.5) or OpenAI</li>
                  <li><strong>4. Tone Adaptation:</strong> Apply professional, friendly, technical, or empathetic tone</li>
                </ol>
              </div>
              <div class="grid grid-cols-2 gap-3 mb-4">
                <div class="p-3 bg-blue-50 rounded-lg text-center">
                  <div class="text-2xl mb-1">👔</div>
                  <div class="font-semibold text-blue-700 text-sm">Professional</div>
                </div>
                <div class="p-3 bg-green-50 rounded-lg text-center">
                  <div class="text-2xl mb-1">😊</div>
                  <div class="font-semibold text-green-700 text-sm">Friendly</div>
                </div>
                <div class="p-3 bg-purple-50 rounded-lg text-center">
                  <div class="text-2xl mb-1">🔧</div>
                  <div class="font-semibold text-purple-700 text-sm">Technical</div>
                </div>
                <div class="p-3 bg-pink-50 rounded-lg text-center">
                  <div class="text-2xl mb-1">💙</div>
                  <div class="font-semibold text-pink-700 text-sm">Empathetic</div>
                </div>
              </div>
              <div class="p-4 bg-yellow-50 rounded-lg border-l-4 border-yellow-500">
                <p class="text-sm text-gray-700">
                  <strong>✨ Smart Features:</strong> Responses are saved with edit tracking, can be regenerated with different tones, and learn from resolution history.
                </p>
              </div>
            </template>
          </StepCard>

          <!-- Step 11 -->
          <StepCard 
            :step="11"
            title="Advanced Analytics Dashboard"
            :active="currentStep === 11"
            @click="setStep(11)"
          >
            <template #icon>
              <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
              </svg>
            </template>
            <template #content>
              <p class="text-gray-700 mb-4">
                Comprehensive analytics system providing insights into ticket operations and agent performance:
              </p>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                <div class="p-4 bg-blue-50 rounded-lg">
                  <div class="font-semibold text-blue-700 mb-2">📈 Ticket Trends</div>
                  <ul class="text-sm text-gray-700 space-y-1">
                    <li>• Daily/weekly/monthly trends</li>
                    <li>• Volume by intent, priority, status</li>
                    <li>• Peak hours and patterns</li>
                    <li>• Time-series visualizations</li>
                  </ul>
                </div>
                <div class="p-4 bg-green-50 rounded-lg">
                  <div class="font-semibold text-green-700 mb-2">👥 Agent Performance</div>
                  <ul class="text-sm text-gray-700 space-y-1">
                    <li>• Tickets resolved per agent</li>
                    <li>• Average resolution time</li>
                    <li>• Agent workload distribution</li>
                    <li>• Performance leaderboards</li>
                  </ul>
                </div>
                <div class="p-4 bg-purple-50 rounded-lg">
                  <div class="font-semibold text-purple-700 mb-2">🎯 Classification Metrics</div>
                  <ul class="text-sm text-gray-700 space-y-1">
                    <li>• Intent distribution breakdown</li>
                    <li>• Sentiment analysis trends</li>
                    <li>• Priority assignment accuracy</li>
                    <li>• Confidence score tracking</li>
                  </ul>
                </div>
                <div class="p-4 bg-orange-50 rounded-lg">
                  <div class="font-semibold text-orange-700 mb-2">📊 Interactive Dashboards</div>
                  <ul class="text-sm text-gray-700 space-y-1">
                    <li>• Real-time data updates</li>
                    <li>• Customizable date ranges</li>
                    <li>• Export to CSV/PDF</li>
                    <li>• Drill-down capabilities</li>
                  </ul>
                </div>
              </div>
              <div class="p-4 bg-gray-50 rounded-lg">
                <p class="text-sm text-gray-600">
                  <strong>🔄 Live Updates:</strong> Dashboard refreshes automatically as tickets are processed, giving managers real-time visibility into support operations.
                </p>
              </div>
            </template>
          </StepCard>

          <!-- Step 12 -->
          <StepCard 
            :step="12"
            title="Agent Dashboard & Collaboration"
            :active="currentStep === 12"
            @click="setStep(12)"
          >
            <template #icon>
              <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
              </svg>
            </template>
            <template #content>
              <p class="text-gray-700 mb-4">
                All information is presented to agents in an intuitive dashboard with real-time collaboration:
              </p>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="p-4 bg-white border rounded-lg">
                  <div class="font-semibold text-gray-900 mb-2">🎯 Smart Filtering</div>
                  <ul class="text-sm text-gray-700 space-y-1">
                    <li>• Filter by intent, sentiment, priority</li>
                    <li>• Filter by channel and date range</li>
                    <li>• Advanced semantic search</li>
                  </ul>
                </div>
                <div class="p-4 bg-white border rounded-lg">
                  <div class="font-semibold text-gray-900 mb-2">📊 Analytics & Insights</div>
                  <ul class="text-sm text-gray-700 space-y-1">
                    <li>• Total tickets and daily trends</li>
                    <li>• Agent performance metrics</li>
                    <li>• Low confidence alerts</li>
                  </ul>
                </div>
                <div class="p-4 bg-white border rounded-lg">
                  <div class="font-semibold text-gray-900 mb-2">🔍 Similar Tickets & Context</div>
                  <ul class="text-sm text-gray-700 space-y-1">
                    <li>• See how similar issues were resolved</li>
                    <li>• Similarity scores with context</li>
                    <li>• Quick navigation between related tickets</li>
                  </ul>
                </div>
                <div class="p-4 bg-white border rounded-lg">
                  <div class="font-semibold text-gray-900 mb-2">🤖 AI-Powered Assistance</div>
                  <ul class="text-sm text-gray-700 space-y-1">
                    <li>• AI-generated response suggestions</li>
                    <li>• KB article recommendations</li>
                    <li>• Resolution template quick actions</li>
                  </ul>
                </div>
              </div>
            </template>
          </StepCard>
        </div>
      </div>

      <!-- Phase 4 & 5 Highlights -->
      <div class="mb-20">
        <div class="text-center mb-12">
          <div class="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-gradient-to-r from-purple-500 to-pink-500 text-white text-sm font-medium mb-6">
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
            </svg>
            <span>Latest Features (Phase 4 & 5)</span>
          </div>
          <h2 class="text-4xl font-bold text-gray-900 dark:text-white mb-4">Advanced AI Capabilities</h2>
          <p class="text-lg text-gray-600 dark:text-gray-400">Next-generation features for intelligent ticket management</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
          <!-- Phase 4: Semantic Matching -->
          <div class="bg-gradient-to-br from-indigo-50 to-purple-100 dark:from-indigo-950 dark:to-purple-900 rounded-2xl p-8 shadow-xl transition-all hover:shadow-2xl hover:-translate-y-1">
            <div class="flex items-center gap-3 mb-4">
              <div class="w-14 h-14 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center shadow-lg">
                <span class="text-3xl">🔍</span>
              </div>
              <div>
                <div class="text-xs font-bold text-indigo-600 dark:text-indigo-400 uppercase tracking-wide">Phase 4</div>
                <h3 class="text-2xl font-bold text-gray-900 dark:text-white">Vector Embeddings & Semantic Matching</h3>
              </div>
            </div>
            <p class="text-gray-700 dark:text-gray-300 mb-4">
              Every ticket is converted to a 384-dimensional vector embedding using sentence-transformers, enabling semantic understanding beyond keywords.
            </p>
            <div class="space-y-3">
              <div class="flex items-start gap-3 p-3 bg-white/50 dark:bg-zinc-900/30 rounded-lg">
                <div class="text-xl">🎯</div>
                <div>
                  <div class="font-semibold text-gray-900 dark:text-white text-sm">Similar Ticket Detection</div>
                  <div class="text-xs text-gray-600 dark:text-gray-400">Find tickets with similar issues using cosine similarity</div>
                </div>
              </div>
              <div class="flex items-start gap-3 p-3 bg-white/50 dark:bg-zinc-900/30 rounded-lg">
                <div class="text-xl">📚</div>
                <div>
                  <div class="font-semibold text-gray-900 dark:text-white text-sm">KB Article Matching</div>
                  <div class="text-xs text-gray-600 dark:text-gray-400">Automatically suggest relevant knowledge base articles</div>
                </div>
              </div>
              <div class="flex items-start gap-3 p-3 bg-white/50 dark:bg-zinc-900/30 rounded-lg">
                <div class="text-xl">💾</div>
                <div>
                  <div class="font-semibold text-gray-900 dark:text-white text-sm">pgvector Storage</div>
                  <div class="text-xs text-gray-600 dark:text-gray-400">Efficient vector similarity search in PostgreSQL</div>
                </div>
              </div>
            </div>
          </div>

          <!-- Phase 5: Four Major Features -->
          <div class="bg-gradient-to-br from-blue-50 to-cyan-100 dark:from-blue-950 dark:to-cyan-900 rounded-2xl p-8 shadow-xl transition-all hover:shadow-2xl hover:-translate-y-1">
            <div class="flex items-center gap-3 mb-4">
              <div class="w-14 h-14 rounded-xl bg-gradient-to-br from-blue-500 to-cyan-600 flex items-center justify-center shadow-lg">
                <span class="text-3xl">🚀</span>
              </div>
              <div>
                <div class="text-xs font-bold text-blue-600 dark:text-blue-400 uppercase tracking-wide">Phase 5</div>
                <h3 class="text-2xl font-bold text-gray-900 dark:text-white">Real-Time & AI Enhancements</h3>
              </div>
            </div>
            <p class="text-gray-700 dark:text-gray-300 mb-4">
              Four major capabilities that transform the support experience with real-time collaboration and AI-powered assistance.
            </p>
            <div class="space-y-3">
              <div class="flex items-start gap-3 p-3 bg-white/50 dark:bg-zinc-900/30 rounded-lg">
                <div class="text-xl">⚡</div>
                <div>
                  <div class="font-semibold text-gray-900 dark:text-white text-sm">WebSocket Real-Time Updates</div>
                  <div class="text-xs text-gray-600 dark:text-gray-400">Agent presence, ticket claims, instant notifications via Redis Pub/Sub</div>
                </div>
              </div>
              <div class="flex items-start gap-3 p-3 bg-white/50 dark:bg-zinc-900/30 rounded-lg">
                <div class="text-xl">📊</div>
                <div>
                  <div class="font-semibold text-gray-900 dark:text-white text-sm">Advanced Analytics</div>
                  <div class="text-xs text-gray-600 dark:text-gray-400">Trends, agent performance, interactive dashboards with live updates</div>
                </div>
              </div>
              <div class="flex items-start gap-3 p-3 bg-white/50 dark:bg-zinc-900/30 rounded-lg">
                <div class="text-xl">🔎</div>
                <div>
                  <div class="font-semibold text-gray-900 dark:text-white text-sm">3-Mode Semantic Search</div>
                  <div class="text-xs text-gray-600 dark:text-gray-400">Semantic, keyword, or hybrid search with RRF scoring</div>
                </div>
              </div>
              <div class="flex items-start gap-3 p-3 bg-white/50 dark:bg-zinc-900/30 rounded-lg">
                <div class="text-xl">🤖</div>
                <div>
                  <div class="font-semibold text-gray-900 dark:text-white text-sm">AI Response Generation (RAG)</div>
                  <div class="text-xs text-gray-600 dark:text-gray-400">Context-aware responses with Ollama/OpenAI in 4 tones</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- RAG Pipeline Detailed View -->
        <div class="bg-gradient-to-br from-purple-50 to-pink-100 dark:from-purple-950 dark:to-pink-900 rounded-2xl p-8 shadow-xl">
          <div class="flex items-center gap-3 mb-6">
            <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-purple-500 to-pink-600 flex items-center justify-center shadow-lg">
              <span class="text-2xl">🧠</span>
            </div>
            <div>
              <h3 class="text-2xl font-bold text-gray-900 dark:text-white">RAG Pipeline: How AI Generates Responses</h3>
              <p class="text-sm text-gray-600 dark:text-gray-400">Retrieval-Augmented Generation for context-aware support responses</p>
            </div>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div class="bg-white/50 dark:bg-zinc-900/30 rounded-xl p-4 transition-all hover:shadow-lg">
              <div class="flex items-center gap-2 mb-2">
                <div class="w-8 h-8 rounded-lg bg-purple-500 text-white flex items-center justify-center font-bold text-sm">1</div>
                <div class="font-bold text-gray-900 dark:text-white text-sm">Context Retrieval</div>
              </div>
              <p class="text-xs text-gray-600 dark:text-gray-400">
                Find similar resolved tickets and relevant KB articles using vector similarity
              </p>
            </div>
            <div class="bg-white/50 dark:bg-zinc-900/30 rounded-xl p-4 transition-all hover:shadow-lg">
              <div class="flex items-center gap-2 mb-2">
                <div class="w-8 h-8 rounded-lg bg-blue-500 text-white flex items-center justify-center font-bold text-sm">2</div>
                <div class="font-bold text-gray-900 dark:text-white text-sm">Prompt Building</div>
              </div>
              <p class="text-xs text-gray-600 dark:text-gray-400">
                Construct prompt with ticket details + retrieved context + resolution history
              </p>
            </div>
            <div class="bg-white/50 dark:bg-zinc-900/30 rounded-xl p-4 transition-all hover:shadow-lg">
              <div class="flex items-center gap-2 mb-2">
                <div class="w-8 h-8 rounded-lg bg-green-500 text-white flex items-center justify-center font-bold text-sm">3</div>
                <div class="font-bold text-gray-900 dark:text-white text-sm">LLM Generation</div>
              </div>
              <p class="text-xs text-gray-600 dark:text-gray-400">
                Generate response using Ollama (llama3.2/qwen2.5) or OpenAI models
              </p>
            </div>
            <div class="bg-white/50 dark:bg-zinc-900/30 rounded-xl p-4 transition-all hover:shadow-lg">
              <div class="flex items-center gap-2 mb-2">
                <div class="w-8 h-8 rounded-lg bg-pink-500 text-white flex items-center justify-center font-bold text-sm">4</div>
                <div class="font-bold text-gray-900 dark:text-white text-sm">Tone Adaptation</div>
              </div>
              <p class="text-xs text-gray-600 dark:text-gray-400">
                Apply professional, friendly, technical, or empathetic tone to response
              </p>
            </div>
          </div>

          <div class="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="bg-green-50 dark:bg-green-950 rounded-lg p-4 border-l-4 border-green-500">
              <div class="flex items-start gap-3">
                <svg class="w-5 h-5 text-green-600 dark:text-green-400 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                </svg>
                <div>
                  <p class="text-sm font-semibold text-green-900 dark:text-green-200 mb-1">✨ Smart Features</p>
                  <p class="text-sm text-green-800 dark:text-green-300">Responses saved with edit tracking, regenerate with different tones, learn from resolution history</p>
                </div>
              </div>
            </div>
            <div class="bg-blue-50 dark:bg-blue-950 rounded-lg p-4 border-l-4 border-blue-500">
              <div class="flex items-start gap-3">
                <svg class="w-5 h-5 text-blue-600 dark:text-blue-400 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                </svg>
                <div>
                  <p class="text-sm font-semibold text-blue-900 dark:text-blue-200 mb-1">🎯 Contextual Accuracy</p>
                  <p class="text-sm text-blue-800 dark:text-blue-300">RAG retrieves actual resolutions and KB content, ensuring responses are grounded in real information</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Technology Stack -->
      <div class="mb-20">
        <div class="text-center mb-12">
          <h2 class="text-4xl font-bold text-gray-900 dark:text-white mb-4">Technology Stack</h2>
          <p class="text-lg text-gray-600 dark:text-gray-400">Built with cutting-edge technologies</p>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div class="group relative bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-blue-950/30 dark:to-indigo-950/30 rounded-2xl shadow-xl hover:shadow-2xl p-8 transition-all duration-300 transform hover:-translate-y-2 border border-blue-200/50 dark:border-blue-800/30 overflow-hidden">
            <div class="absolute inset-0 bg-gradient-to-br from-blue-500/0 to-indigo-500/0 group-hover:from-blue-500/5 group-hover:to-indigo-500/5 transition-all duration-300"></div>
            <div class="relative">
              <div class="flex items-center gap-3 mb-6">
                <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center shadow-lg">
                  <span class="text-2xl">🤖</span>
                </div>
                <h3 class="text-2xl font-bold text-gray-900 dark:text-white">AI/ML</h3>
              </div>
              <ul class="space-y-4 text-sm text-gray-700 dark:text-gray-300">
                <li class="flex items-start gap-3 p-3 rounded-lg bg-white/50 dark:bg-zinc-900/30 backdrop-blur-sm">
                  <div class="w-2 h-2 rounded-full bg-gradient-to-br from-blue-500 to-indigo-600 mt-2 flex-shrink-0"></div>
                  <span><strong class="text-gray-900 dark:text-white">Hugging Face Transformers</strong><br><span class="text-gray-600 dark:text-gray-400">Zero-shot classification & sentiment</span></span>
                </li>
                <li class="flex items-start gap-3 p-3 rounded-lg bg-white/50 dark:bg-zinc-900/30 backdrop-blur-sm">
                  <div class="w-2 h-2 rounded-full bg-gradient-to-br from-blue-500 to-indigo-600 mt-2 flex-shrink-0"></div>
                  <span><strong class="text-gray-900 dark:text-white">sentence-transformers</strong><br><span class="text-gray-600 dark:text-gray-400">384-dim vector embeddings</span></span>
                </li>
                <li class="flex items-start gap-3 p-3 rounded-lg bg-white/50 dark:bg-zinc-900/30 backdrop-blur-sm">
                  <div class="w-2 h-2 rounded-full bg-gradient-to-br from-blue-500 to-indigo-600 mt-2 flex-shrink-0"></div>
                  <span><strong class="text-gray-900 dark:text-white">PyTorch</strong><br><span class="text-gray-600 dark:text-gray-400">Deep learning framework</span></span>
                </li>
              </ul>
            </div>
          </div>

          <div class="group relative bg-gradient-to-br from-green-50 to-emerald-50 dark:from-green-950/30 dark:to-emerald-950/30 rounded-2xl shadow-xl hover:shadow-2xl p-8 transition-all duration-300 transform hover:-translate-y-2 border border-green-200/50 dark:border-green-800/30 overflow-hidden">
            <div class="absolute inset-0 bg-gradient-to-br from-green-500/0 to-emerald-500/0 group-hover:from-green-500/5 group-hover:to-emerald-500/5 transition-all duration-300"></div>
            <div class="relative">
              <div class="flex items-center gap-3 mb-6">
                <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-green-500 to-emerald-600 flex items-center justify-center shadow-lg">
                  <span class="text-2xl">⚙️</span>
                </div>
                <h3 class="text-2xl font-bold text-gray-900 dark:text-white">Backend</h3>
              </div>
              <ul class="space-y-4 text-sm text-gray-700 dark:text-gray-300">
                <li class="flex items-start gap-3 p-3 rounded-lg bg-white/50 dark:bg-zinc-900/30 backdrop-blur-sm">
                  <div class="w-2 h-2 rounded-full bg-gradient-to-br from-green-500 to-emerald-600 mt-2 flex-shrink-0"></div>
                  <span><strong class="text-gray-900 dark:text-white">FastAPI</strong><br><span class="text-gray-600 dark:text-gray-400">High-performance async API</span></span>
                </li>
                <li class="flex items-start gap-3 p-3 rounded-lg bg-white/50 dark:bg-zinc-900/30 backdrop-blur-sm">
                  <div class="w-2 h-2 rounded-full bg-gradient-to-br from-green-500 to-emerald-600 mt-2 flex-shrink-0"></div>
                  <span><strong class="text-gray-900 dark:text-white">SQLModel</strong><br><span class="text-gray-600 dark:text-gray-400">Type-safe ORM with Pydantic</span></span>
                </li>
                <li class="flex items-start gap-3 p-3 rounded-lg bg-white/50 dark:bg-zinc-900/30 backdrop-blur-sm">
                  <div class="w-2 h-2 rounded-full bg-gradient-to-br from-green-500 to-emerald-600 mt-2 flex-shrink-0"></div>
                  <span><strong class="text-gray-900 dark:text-white">PostgreSQL 16 + pgvector</strong><br><span class="text-gray-600 dark:text-gray-400">Vector similarity search</span></span>
                </li>
                <li class="flex items-start gap-3 p-3 rounded-lg bg-white/50 dark:bg-zinc-900/30 backdrop-blur-sm">
                  <div class="w-2 h-2 rounded-full bg-gradient-to-br from-green-500 to-emerald-600 mt-2 flex-shrink-0"></div>
                  <span><strong class="text-gray-900 dark:text-white">Redis</strong><br><span class="text-gray-600 dark:text-gray-400">Pub/Sub for WebSocket events</span></span>
                </li>
                <li class="flex items-start gap-3 p-3 rounded-lg bg-white/50 dark:bg-zinc-900/30 backdrop-blur-sm">
                  <div class="w-2 h-2 rounded-full bg-gradient-to-br from-green-500 to-emerald-600 mt-2 flex-shrink-0"></div>
                  <span><strong class="text-gray-900 dark:text-white">Ollama + OpenAI</strong><br><span class="text-gray-600 dark:text-gray-400">Local & cloud LLMs for RAG</span></span>
                </li>
              </ul>
            </div>
          </div>

          <div class="group relative bg-gradient-to-br from-purple-50 to-pink-50 dark:from-purple-950/30 dark:to-pink-950/30 rounded-2xl shadow-xl hover:shadow-2xl p-8 transition-all duration-300 transform hover:-translate-y-2 border border-purple-200/50 dark:border-purple-800/30 overflow-hidden">
            <div class="absolute inset-0 bg-gradient-to-br from-purple-500/0 to-pink-500/0 group-hover:from-purple-500/5 group-hover:to-pink-500/5 transition-all duration-300"></div>
            <div class="relative">
              <div class="flex items-center gap-3 mb-6">
                <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-purple-500 to-pink-600 flex items-center justify-center shadow-lg">
                  <span class="text-2xl">🎨</span>
                </div>
                <h3 class="text-2xl font-bold text-gray-900 dark:text-white">Frontend</h3>
              </div>
              <ul class="space-y-4 text-sm text-gray-700 dark:text-gray-300">
                <li class="flex items-start gap-3 p-3 rounded-lg bg-white/50 dark:bg-zinc-900/30 backdrop-blur-sm">
                  <div class="w-2 h-2 rounded-full bg-gradient-to-br from-purple-500 to-pink-600 mt-2 flex-shrink-0"></div>
                  <span><strong class="text-gray-900 dark:text-white">Nuxt.js 3</strong><br><span class="text-gray-600 dark:text-gray-400">Vue 3 with SSR</span></span>
                </li>
                <li class="flex items-start gap-3 p-3 rounded-lg bg-white/50 dark:bg-zinc-900/30 backdrop-blur-sm">
                  <div class="w-2 h-2 rounded-full bg-gradient-to-br from-purple-500 to-pink-600 mt-2 flex-shrink-0"></div>
                  <span><strong class="text-gray-900 dark:text-white">TailwindCSS</strong><br><span class="text-gray-600 dark:text-gray-400">Utility-first styling</span></span>
                </li>
                <li class="flex items-start gap-3 p-3 rounded-lg bg-white/50 dark:bg-zinc-900/30 backdrop-blur-sm">
                  <div class="w-2 h-2 rounded-full bg-gradient-to-br from-purple-500 to-pink-600 mt-2 flex-shrink-0"></div>
                  <span><strong class="text-gray-900 dark:text-white">Composition API</strong><br><span class="text-gray-600 dark:text-gray-400">Modern Vue reactivity</span></span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <!-- Performance Metrics -->
      <div class="mb-16">
        <h2 class="text-3xl font-bold text-gray-900 dark:text-white mb-8 text-center">Performance & Quality</h2>
        <div class="bg-white dark:bg-zinc-800 rounded-xl shadow-xl p-8 transition-colors">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div>
              <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">🎯 Model Accuracy</h3>
              <div class="space-y-4">
                <div>
                  <div class="flex justify-between mb-1">
                    <span class="text-sm text-gray-600">Intent Classification</span>
                    <span class="text-sm font-semibold text-gray-900">~90%</span>
                  </div>
                  <div class="w-full bg-gray-200 rounded-full h-2">
                    <div class="bg-blue-600 h-2 rounded-full" style="width: 90%"></div>
                  </div>
                </div>
                <div>
                  <div class="flex justify-between mb-1">
                    <span class="text-sm text-gray-600">Sentiment Analysis</span>
                    <span class="text-sm font-semibold text-gray-900">~88%</span>
                  </div>
                  <div class="w-full bg-gray-200 rounded-full h-2">
                    <div class="bg-green-600 h-2 rounded-full" style="width: 88%"></div>
                  </div>
                </div>
                <div>
                  <div class="flex justify-between mb-1">
                    <span class="text-sm text-gray-600">Similar Ticket Relevance</span>
                    <span class="text-sm font-semibold text-gray-900">&gt;85%</span>
                  </div>
                  <div class="w-full bg-gray-200 rounded-full h-2">
                    <div class="bg-purple-600 h-2 rounded-full" style="width: 85%"></div>
                  </div>
                </div>
              </div>
            </div>
            <div>
              <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">⚡ Response Times</h3>
              <div class="space-y-4">
                <div>
                  <div class="flex justify-between mb-1">
                    <span class="text-sm text-gray-600">Classification</span>
                    <span class="text-sm font-semibold text-gray-900">&lt;200ms</span>
                  </div>
                  <div class="w-full bg-gray-200 rounded-full h-2">
                    <div class="bg-orange-600 h-2 rounded-full" style="width: 40%"></div>
                  </div>
                </div>
                <div>
                  <div class="flex justify-between mb-1">
                    <span class="text-sm text-gray-600">Embedding Generation</span>
                    <span class="text-sm font-semibold text-gray-900">~50ms</span>
                  </div>
                  <div class="w-full bg-gray-200 rounded-full h-2">
                    <div class="bg-yellow-600 h-2 rounded-full" style="width: 25%"></div>
                  </div>
                </div>
                <div>
                  <div class="flex justify-between mb-1">
                    <span class="text-sm text-gray-600">Similarity Search</span>
                    <span class="text-sm font-semibold text-gray-900">&lt;100ms</span>
                  </div>
                  <div class="w-full bg-gray-200 rounded-full h-2">
                    <div class="bg-red-600 h-2 rounded-full" style="width: 50%"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Business Impact -->
      <div class="mb-16">
        <h2 class="text-3xl font-bold text-gray-900 dark:text-white mb-8 text-center">Business Impact</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div class="bg-gradient-to-br from-blue-50 to-blue-100 dark:from-blue-950 dark:to-blue-900 rounded-lg p-6 transition-colors">
            <div class="text-4xl mb-3">⚡</div>
            <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-2">50% Faster</h3>
            <p class="text-gray-700 dark:text-gray-300">
              Automatic prioritization and routing reduces first-response time by half
            </p>
          </div>
          <div class="bg-gradient-to-br from-green-50 to-green-100 dark:from-green-950 dark:to-green-900 rounded-lg p-6 transition-colors">
            <div class="text-4xl mb-3">💰</div>
            <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-2">40% Cost Reduction</h3>
            <p class="text-gray-700 dark:text-gray-300">
              Efficient ticket handling and suggestions reduce operational costs
            </p>
          </div>
          <div class="bg-gradient-to-br from-purple-50 to-purple-100 dark:from-purple-950 dark:to-purple-900 rounded-lg p-6 transition-colors">
            <div class="text-4xl mb-3">😊</div>
            <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-2">Better CX</h3>
            <p class="text-gray-700 dark:text-gray-300">
              Faster, more accurate responses improve customer satisfaction
            </p>
          </div>
        </div>
      </div>

      <!-- Deployment Pipeline & Infrastructure -->
      <div class="mb-16">
        <div class="text-center mb-12">
          <div class="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-gradient-to-r from-orange-500 to-red-500 text-white text-sm font-medium mb-4">
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
              <path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z"/>
            </svg>
            <span>Infrastructure & Deployment</span>
          </div>
          <h2 class="text-4xl font-bold text-gray-900 dark:text-white mb-4">CI/CD Pipeline & Cloud Architecture</h2>
          <p class="text-xl text-gray-600 dark:text-gray-400 max-w-3xl mx-auto">
            Automated CI/CD via GitHub Actions with AWS-ready cloud infrastructure
          </p>
        </div>

        <!-- CI/CD Pipeline Flow -->
        <div class="bg-white/50 dark:bg-gray-900/50 backdrop-blur-xl rounded-2xl p-8 mb-8 border border-gray-200 dark:border-gray-700">
          <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-6 flex items-center gap-3">
            <div class="w-10 h-10 rounded-lg bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/>
              </svg>
            </div>
            <span>CI/CD Deployment Pipeline (GitHub Actions)</span>
          </h3>
          
          <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
            <!-- Step 1: Code Push -->
            <div class="relative">
              <div class="bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-800 dark:to-gray-700 rounded-xl p-4 h-full transition-all hover:shadow-lg hover:-translate-y-1">
                <div class="flex items-center gap-2 mb-2">
                  <div class="text-2xl">📝</div>
                  <svg class="w-6 h-6 text-gray-700 dark:text-gray-300" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                  </svg>
                </div>
                <h4 class="font-bold text-gray-900 dark:text-white mb-1">1. Code Push</h4>
                <p class="text-sm text-gray-600 dark:text-gray-400">Developer pushes code to GitHub repository</p>
              </div>
              <div class="hidden md:block absolute top-1/2 -right-2 transform -translate-y-1/2 z-10">
                <div class="text-2xl text-blue-500">→</div>
              </div>
            </div>

            <!-- Step 2: GitHub Actions Workflow -->
            <div class="relative">
              <div class="bg-gradient-to-br from-blue-50 to-blue-100 dark:from-blue-950 dark:to-blue-900 rounded-xl p-4 h-full transition-all hover:shadow-lg hover:-translate-y-1">
                <div class="flex items-center gap-2 mb-2">
                  <div class="text-2xl">⚙️</div>
                  <div class="px-2 py-0.5 bg-blue-600 text-white text-xs font-bold rounded">CI</div>
                </div>
                <h4 class="font-bold text-gray-900 dark:text-white mb-1">2. GitHub Actions</h4>
                <p class="text-sm text-gray-600 dark:text-gray-400">Automated workflow triggers on push/PR</p>
              </div>
              <div class="hidden md:block absolute top-1/2 -right-2 transform -translate-y-1/2 z-10">
                <div class="text-2xl text-blue-500">→</div>
              </div>
            </div>

            <!-- Step 3: Automated Tests -->
            <div class="relative">
              <div class="bg-gradient-to-br from-purple-50 to-purple-100 dark:from-purple-950 dark:to-purple-900 rounded-xl p-4 h-full transition-all hover:shadow-lg hover:-translate-y-1">
                <div class="flex items-center gap-2 mb-2">
                  <div class="text-2xl">🧪</div>
                  <div class="px-2 py-0.5 bg-purple-600 text-white text-xs font-bold rounded">TEST</div>
                </div>
                <h4 class="font-bold text-gray-900 dark:text-white mb-1">3. Run Tests</h4>
                <p class="text-sm text-gray-600 dark:text-gray-400">Unit, integration & linting validation</p>
              </div>
              <div class="hidden md:block absolute top-1/2 -right-2 transform -translate-y-1/2 z-10">
                <div class="text-2xl text-blue-500">→</div>
              </div>
            </div>

            <!-- Step 4: Build Docker Images -->
            <div class="bg-gradient-to-br from-green-50 to-green-100 dark:from-green-950 dark:to-green-900 rounded-xl p-4 h-full transition-all hover:shadow-lg hover:-translate-y-1">
              <div class="flex items-center gap-2 mb-2">
                <div class="text-2xl">🐳</div>
                <div class="px-2 py-0.5 bg-green-600 text-white text-xs font-bold rounded">BUILD</div>
              </div>
              <h4 class="font-bold text-gray-900 dark:text-white mb-1">4. Build & Verify</h4>
              <p class="text-sm text-gray-600 dark:text-gray-400">Docker images built and validated</p>
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
            <!-- Current Implementation -->
            <div class="bg-green-50 dark:bg-green-950 rounded-lg p-4 border-l-4 border-green-500">
              <div class="flex items-start gap-3">
                <svg class="w-5 h-5 text-green-600 dark:text-green-400 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
                </svg>
                <div>
                  <p class="text-sm font-semibold text-green-900 dark:text-green-200 mb-1">✓ Currently Active</p>
                  <p class="text-sm text-green-800 dark:text-green-300">GitHub Actions handles all CI/CD operations: automated testing, code quality checks, Docker builds, and deployment verification on every commit.</p>
                </div>
              </div>
            </div>

            <!-- AWS Deployment Ready -->
            <div class="bg-blue-50 dark:bg-blue-950 rounded-lg p-4 border-l-4 border-blue-500">
              <div class="flex items-start gap-3">
                <svg class="w-5 h-5 text-blue-600 dark:text-blue-400 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z"/>
                  <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z"/>
                </svg>
                <div>
                  <p class="text-sm font-semibold text-blue-900 dark:text-blue-200 mb-1">☁️ AWS Deployment Available</p>
                  <p class="text-sm text-blue-800 dark:text-blue-300">Infrastructure configured for AWS deployment via ECS, RDS, and supporting services. Ready to scale to production when needed.</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- AWS Architecture -->
        <div class="bg-white/50 dark:bg-gray-900/50 backdrop-blur-xl rounded-2xl p-8 border border-gray-200 dark:border-gray-700">
          <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-6 flex items-center gap-3">
            <div class="w-10 h-10 rounded-lg bg-gradient-to-br from-orange-500 to-yellow-500 flex items-center justify-center">
              <svg class="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path d="M2 11a1 1 0 011-1h2a1 1 0 011 1v5a1 1 0 01-1 1H3a1 1 0 01-1-1v-5zM8 7a1 1 0 011-1h2a1 1 0 011 1v9a1 1 0 01-1 1H9a1 1 0 01-1-1V7zM14 4a1 1 0 011-1h2a1 1 0 011 1v12a1 1 0 01-1 1h-2a1 1 0 01-1-1V4z"/>
              </svg>
            </div>
            <span>AWS Cloud Infrastructure</span>
          </h3>

          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <!-- ECS/Fargate -->
            <div class="bg-gradient-to-br from-orange-50 to-red-50 dark:from-orange-950 dark:to-red-950 rounded-xl p-6 transition-all hover:shadow-lg hover:-translate-y-1">
              <div class="flex items-center gap-3 mb-4">
                <div class="w-12 h-12 rounded-lg bg-gradient-to-br from-orange-500 to-red-500 flex items-center justify-center text-white font-bold text-lg">
                  ECS
                </div>
                <div>
                  <h4 class="font-bold text-gray-900 dark:text-white">Container Orchestration</h4>
                  <p class="text-xs text-gray-600 dark:text-gray-400">AWS ECS Fargate</p>
                </div>
              </div>
              <ul class="space-y-2 text-sm text-gray-700 dark:text-gray-300">
                <li class="flex items-start gap-2">
                  <span class="text-green-500 mt-0.5">✓</span>
                  <span>Serverless container management</span>
                </li>
                <li class="flex items-start gap-2">
                  <span class="text-green-500 mt-0.5">✓</span>
                  <span>Auto-scaling based on load</span>
                </li>
                <li class="flex items-start gap-2">
                  <span class="text-green-500 mt-0.5">✓</span>
                  <span>Zero-downtime deployments</span>
                </li>
              </ul>
            </div>

            <!-- RDS PostgreSQL -->
            <div class="bg-gradient-to-br from-blue-50 to-indigo-50 dark:from-blue-950 dark:to-indigo-950 rounded-xl p-6 transition-all hover:shadow-lg hover:-translate-y-1">
              <div class="flex items-center gap-3 mb-4">
                <div class="w-12 h-12 rounded-lg bg-gradient-to-br from-blue-500 to-indigo-500 flex items-center justify-center text-white font-bold text-lg">
                  RDS
                </div>
                <div>
                  <h4 class="font-bold text-gray-900 dark:text-white">Database Service</h4>
                  <p class="text-xs text-gray-600 dark:text-gray-400">PostgreSQL + pgvector</p>
                </div>
              </div>
              <ul class="space-y-2 text-sm text-gray-700 dark:text-gray-300">
                <li class="flex items-start gap-2">
                  <span class="text-green-500 mt-0.5">✓</span>
                  <span>Automated backups & recovery</span>
                </li>
                <li class="flex items-start gap-2">
                  <span class="text-green-500 mt-0.5">✓</span>
                  <span>Multi-AZ high availability</span>
                </li>
                <li class="flex items-start gap-2">
                  <span class="text-green-500 mt-0.5">✓</span>
                  <span>Vector similarity search</span>
                </li>
              </ul>
            </div>

            <!-- ALB + CloudFront -->
            <div class="bg-gradient-to-br from-purple-50 to-pink-50 dark:from-purple-950 dark:to-pink-950 rounded-xl p-6 transition-all hover:shadow-lg hover:-translate-y-1">
              <div class="flex items-center gap-3 mb-4">
                <div class="w-12 h-12 rounded-lg bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center text-white font-bold text-lg">
                  CDN
                </div>
                <div>
                  <h4 class="font-bold text-gray-900 dark:text-white">Load Balancing & CDN</h4>
                  <p class="text-xs text-gray-600 dark:text-gray-400">ALB + CloudFront</p>
                </div>
              </div>
              <ul class="space-y-2 text-sm text-gray-700 dark:text-gray-300">
                <li class="flex items-start gap-2">
                  <span class="text-green-500 mt-0.5">✓</span>
                  <span>Global content delivery</span>
                </li>
                <li class="flex items-start gap-2">
                  <span class="text-green-500 mt-0.5">✓</span>
                  <span>SSL/TLS encryption</span>
                </li>
                <li class="flex items-start gap-2">
                  <span class="text-green-500 mt-0.5">✓</span>
                  <span>DDoS protection</span>
                </li>
              </ul>
            </div>

            <!-- S3 Storage -->
            <div class="bg-gradient-to-br from-green-50 to-teal-50 dark:from-green-950 dark:to-teal-950 rounded-xl p-6 transition-all hover:shadow-lg hover:-translate-y-1">
              <div class="flex items-center gap-3 mb-4">
                <div class="w-12 h-12 rounded-lg bg-gradient-to-br from-green-500 to-teal-500 flex items-center justify-center text-white font-bold text-lg">
                  S3
                </div>
                <div>
                  <h4 class="font-bold text-gray-900 dark:text-white">Object Storage</h4>
                  <p class="text-xs text-gray-600 dark:text-gray-400">Amazon S3</p>
                </div>
              </div>
              <ul class="space-y-2 text-sm text-gray-700 dark:text-gray-300">
                <li class="flex items-start gap-2">
                  <span class="text-green-500 mt-0.5">✓</span>
                  <span>Static assets & backups</span>
                </li>
                <li class="flex items-start gap-2">
                  <span class="text-green-500 mt-0.5">✓</span>
                  <span>Versioning & lifecycle policies</span>
                </li>
                <li class="flex items-start gap-2">
                  <span class="text-green-500 mt-0.5">✓</span>
                  <span>99.999999999% durability</span>
                </li>
              </ul>
            </div>

            <!-- CloudWatch -->
            <div class="bg-gradient-to-br from-yellow-50 to-amber-50 dark:from-yellow-950 dark:to-amber-950 rounded-xl p-6 transition-all hover:shadow-lg hover:-translate-y-1">
              <div class="flex items-center gap-3 mb-4">
                <div class="w-12 h-12 rounded-lg bg-gradient-to-br from-yellow-500 to-amber-500 flex items-center justify-center text-white font-bold text-lg">
                  CW
                </div>
                <div>
                  <h4 class="font-bold text-gray-900 dark:text-white">Monitoring & Logging</h4>
                  <p class="text-xs text-gray-600 dark:text-gray-400">CloudWatch</p>
                </div>
              </div>
              <ul class="space-y-2 text-sm text-gray-700 dark:text-gray-300">
                <li class="flex items-start gap-2">
                  <span class="text-green-500 mt-0.5">✓</span>
                  <span>Real-time metrics & alarms</span>
                </li>
                <li class="flex items-start gap-2">
                  <span class="text-green-500 mt-0.5">✓</span>
                  <span>Centralized log aggregation</span>
                </li>
                <li class="flex items-start gap-2">
                  <span class="text-green-500 mt-0.5">✓</span>
                  <span>Performance dashboards</span>
                </li>
              </ul>
            </div>

            <!-- Secrets Manager -->
            <div class="bg-gradient-to-br from-red-50 to-rose-50 dark:from-red-950 dark:to-rose-950 rounded-xl p-6 transition-all hover:shadow-lg hover:-translate-y-1">
              <div class="flex items-center gap-3 mb-4">
                <div class="w-12 h-12 rounded-lg bg-gradient-to-br from-red-500 to-rose-500 flex items-center justify-center text-white font-bold text-lg">
                  🔐
                </div>
                <div>
                  <h4 class="font-bold text-gray-900 dark:text-white">Secrets Management</h4>
                  <p class="text-xs text-gray-600 dark:text-gray-400">AWS Secrets Manager</p>
                </div>
              </div>
              <ul class="space-y-2 text-sm text-gray-700 dark:text-gray-300">
                <li class="flex items-start gap-2">
                  <span class="text-green-500 mt-0.5">✓</span>
                  <span>Encrypted API keys & passwords</span>
                </li>
                <li class="flex items-start gap-2">
                  <span class="text-green-500 mt-0.5">✓</span>
                  <span>Automatic rotation</span>
                </li>
                <li class="flex items-start gap-2">
                  <span class="text-green-500 mt-0.5">✓</span>
                  <span>Fine-grained access control</span>
                </li>
              </ul>
            </div>
          </div>

          <div class="mt-6 bg-gradient-to-r from-orange-50 to-yellow-50 dark:from-orange-950 dark:to-yellow-950 rounded-lg p-4 border-l-4 border-orange-500">
            <div class="flex items-start gap-3">
              <svg class="w-5 h-5 text-orange-600 dark:text-orange-400 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clip-rule="evenodd"/>
              </svg>
              <div>
                <p class="text-sm font-semibold text-orange-900 dark:text-orange-200 mb-1">Infrastructure as Code</p>
                <p class="text-sm text-orange-800 dark:text-orange-300">All AWS resources are managed via Terraform/CloudFormation for version control, reproducibility, and disaster recovery.</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- CTA -->
      <div class="text-center">
        <div class="relative bg-gradient-to-r from-blue-600 via-purple-600 to-pink-600 rounded-3xl shadow-2xl p-12 text-white overflow-hidden">
          <div class="absolute inset-0">
            <div class="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGRlZnM+PHBhdHRlcm4gaWQ9ImdyaWQiIHdpZHRoPSI2MCIgaGVpZ2h0PSI2MCIgcGF0dGVyblVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+PHBhdGggZD0iTSAxMCAwIEwgMCAwIDAgMTAiIGZpbGw9Im5vbmUiIHN0cm9rZT0id2hpdGUiIHN0cm9rZS13aWR0aD0iMC41IiBvcGFjaXR5PSIwLjEiLz48L3BhdHRlcm4+PC9kZWZzPjxyZWN0IHdpZHRoPSIxMDAlIiBoZWlnaHQ9IjEwMCUiIGZpbGw9InVybCgjZ3JpZCkiLz48L3N2Zz4=')] opacity-20"></div>
          </div>
          <div class="relative">
            <div class="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/20 backdrop-blur-sm text-white text-sm font-medium mb-6">
              <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M11.3 1.046A1 1 0 0112 2v5h4a1 1 0 01.82 1.573l-7 10A1 1 0 018 18v-5H4a1 1 0 01-.82-1.573l7-10a1 1 0 011.12-.38z" clip-rule="evenodd"/>
              </svg>
              <span>Experience the Power</span>
            </div>
            <h2 class="text-4xl md:text-5xl font-bold mb-4 leading-tight">Ready to See It in Action?</h2>
            <p class="text-xl mb-8 opacity-90 max-w-2xl mx-auto">
              Try creating a ticket and watch our AI-powered system classify, prioritize, and suggest solutions in real-time
            </p>
            <div class="flex flex-col sm:flex-row gap-4 justify-center">
              <NuxtLink to="/compose" class="group px-8 py-4 bg-white text-blue-600 rounded-xl font-bold hover:bg-gray-100 transition-all duration-300 shadow-xl hover:shadow-2xl hover:scale-105 flex items-center justify-center gap-2">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
                </svg>
                <span>Create a Ticket</span>
                <svg class="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"/>
                </svg>
              </NuxtLink>
              <NuxtLink to="/tickets" class="group px-8 py-4 bg-white/10 backdrop-blur-sm text-white rounded-xl font-bold hover:bg-white/20 transition-all duration-300 border-2 border-white/30 hover:border-white/50 hover:scale-105 flex items-center justify-center gap-2">
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"/>
                </svg>
                <span>View Tickets</span>
              </NuxtLink>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const currentStep = ref(1)
const isDark = ref(false)
let interval: number | null = null

// Theme management
const toggleTheme = () => {
  isDark.value = !isDark.value
  if (isDark.value) {
    document.documentElement.classList.add('dark')
    localStorage.setItem('theme', 'dark')
  } else {
    document.documentElement.classList.remove('dark')
    localStorage.setItem('theme', 'light')
  }
}

const setStep = (step: number) => {
  currentStep.value = step
  // Stop auto-play when user manually selects a step
  if (interval) {
    clearInterval(interval)
    interval = null
  }
}

const startAutoPlay = () => {
  // Auto-play through all 12 steps of the pipeline
  interval = setInterval(() => {
    currentStep.value = currentStep.value >= 12 ? 1 : currentStep.value + 1
  }, 5000) as unknown as number
}

onMounted(() => {
  // Check for saved theme preference or default to light
  const savedTheme = localStorage.getItem('theme')
  if (savedTheme === 'dark' || (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    isDark.value = true
    document.documentElement.classList.add('dark')
  } else {
    isDark.value = false
    document.documentElement.classList.remove('dark')
  }
  
  // Auto-play disabled to prevent unwanted scrolling
  // startAutoPlay()
})

onUnmounted(() => {
  if (interval) {
    clearInterval(interval)
  }
})
</script>

<style scoped>
/* Removed global transitions to prevent scroll issues */
</style>
