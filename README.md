# Journal
### A journaling assistant
> [!Note]
> The unexamined life is not worth living -- Socrate

Journaling has many benefits including clarity of thought and feeling less overwhelmed but getting into the habit has many frictions including what, where and how to write, and then how to gain insights from previous writings. Those who succeed in this do so by being super organized and disciplined, but lacking organization and discipline should not prevent us from having clarity and feeling less overwhelmed. Solving this problem is what this project is about.

The goal is to build a simple tool that facilitates daily journaling.

## The MVP
The first iteration will be a CLI chat app with A.I assistance. The advantage is that the UI can be simple, you can access it easily and the model could be open-source and run locally, if practical. These requirements might change depending on the needs. 

## Initial Design
The user flow:
1. **Start session**: a session is your daily window of time when you need to journal. For 5-10 minutes you have to write a certain number of words about how the day went, how you felt in general, what went well, what can be improved, what ideas crossed your mind, what thoughts. If you've not writen enough, the assistant should ask questions, should be like a discussion with a friend or coach, the style, tone, etc... will depend on the user's needs. <br>After the session, your entries are organized by the a.i, insights are extracted and saved as context for the future.
3. **Reviews**: every sunday, you can review the week. Chat about what happened, what went well, what didn't, etc... Same for end of month, mi-year and end of year. 

