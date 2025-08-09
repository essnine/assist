# Assist
I started this thing as a job runner sort of program I want running on my older laptop I run linux on at home. The notion of it is that I want to write code that I can run periodically or schedule for a one-off, and just not have to think about it. I know Cron jobs and scheduling libraries exist, but creating this myself is also an exercise in understanding how to design a system that wants to work this way, and also maybe possibly letting it interact with itself.

Anyway.

The first thing I wanted to create was a mail-to-kindle type of thing that could run on a daily basis to sync books to my Kindle without me having to manually run the whole process. As of now, it runs on the Quart framework, accepting GET and POST requests on `/tasks` to view and add tasks respectively. The kindle task is present but yet to be tested.

## Why am I making this?
Honestly, I wanted to make something like this at work ages ago, when building out some automation for creating search indexes on a platform running on Kubernetes. With some senior colleagues' input and a little curiosity, I ended up using Argo Workflows for that task, but all-in-all, our implementation seemed like overkill then and still does now. A lot of ML work is deep magic happening inside precomplied binaries that we hit with python wrappers, and doing K-native stuff just for orchestrating stuff that's happening over API calls anyway doesn't feel right. So, here. General purpose automation. For my own little computer tings for now.

## TODOs:
✅ Add Demo Task template

- Add Scheduled Ping Task template

- Add One-Off Ping Task template

- Add Custom Code Runner template

- Maybe play around with letting tasks call other tasks

