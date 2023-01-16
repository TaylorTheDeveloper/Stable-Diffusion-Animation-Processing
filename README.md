
![Teaser](/documentation/images/0003.gif)

# Stable-Diffusion-Animation-Processing

This is my workflow for generating beautiful, semi-temporally-coherent videos using stable diffusion and a few other tools.

My goal is to help speed up the adoption of this technology and improve its viability for professional use and commercial applications across filmmaking, marketing, and more. I believe that these tools should be open source and publicly available and encourage others to do the same.

There are limitations due to the nature of the diffusion process- outputs tend to favor randomness. This makes for fantastic still artwork- but animations are challenging. I've tried to make this guide as user friendly as possible, however expect to set up and configure a few things! You can get in touch with me below or through PRs here if you have questions.

PRs will be reviewed- so if you develop cool prompts with this process please share them here! This page and guide will only be updated with well vetted process changes, so please be prepared for that!

A big thank you to the AI community, AI researchers who've spent years developing these and other AI models, and the netizens who have been contributing and sharing their learning with each other online. This repo is dedicated to all of you and your contributions. 

# Contact 

- You can find me on discord here: TemporalCoherence#2744
- I hang out in the animation group here: https://discord.gg/stablediffusion

# Processing Steps

## Step 1: Find a good video
1. Avoid videos where the focus is changing or going in and out.
2. videos with terrible lighting or a lot of noise.
3. Movement is ok, but very fast blurry movement will increase randomness of output and should be avoided.
4. Recommend MP4 or WebM videos. However I have also worked with MTS format successfully, but it's less popular.
5. Make sure to get these video details for use later:
Video height and width (Step 3), and FPS (Step 2)

## Step 2: Background Extraction (Optional but recommended)

This is optional, and if you want- you can skip this step!

I find the backgrounds of videos to be very distracting. Most uncontrolled random artifacts come from the background, so I often opt to remove them to eliminate noise. This makes it very easy to composite your subject over a new background later. 

[PeterL1n has an awesome github project](https://github.com/PeterL1n/RobustVideoMatting) that makes this easy. I forked it to enable a color setting option and when he accepts my PR I will update these docs to point back to his repo. 

- Until then, you can find the modified [source code here](https://github.com/TaylorTheDeveloper/RobustVideoMatting)

- And you can use the [google collab right now](https://colab.research.google.com/drive/11ERb04vWXy5YhSyCqejaaoBFEwIzinAT?usp=share_link) to remove your background a replace with any color

## Step 3: Frame Extraction
1. Use FFMPEG and extract frames. I use Windows but use ffmpeg through the Windows Subsystem for Linux, but you can also just use.
2. 24 FPS is ideal. While you can go higher or lower and modify it for interpolation later, I generally stay at 24 FPS. However sometimes it makes sense to generate more frames, depending on the input video frame rate. For example, if you want to match slow motion 120 FPS... then do that! It will take about 5 times longer to get your output due to increased frame counts.
3. Extract these videos to a new folder called 'raw' or 'src' so they don't get mixed in with other results. This folder must be created before you run ffmpeg.

FFMpeg command for 24 FPS: `ffmpeg -r 24 raw/out%03d.png -i input.mp4`

## Step 4: Stable Diffusion 
1. Make sure your using Stable Diffusion Web UI! https://github.com/AUTOMATIC1111/stable-diffusion-webui
    - [Getting started Guide for Automatic1111](https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/Install-and-Run-on-NVidia-GPUs)
2. See Prompts/core.prompt for specific details on settings that I used for Stable Diffusion. 
    - As I create more prompt configurations, I will upload them here! If you have some to share, I will accept pull requests!
    - While not expressly required, I like to make sure the source width/height and output width/hight are the same. If you want to match outputs closely, aspect ratio should be the same or close. 
       - An aside: With content on the web, quality and bit rate/depth varies widely. So if videos are lower quality I generally will render them out with increased heights and widths. If 240x320 video then make sure the settings match or are higher, for example I may got with 480x640 or even 960x1280.For 1920x1080, however, I generally keep it the same. This rule may not apply to you if you use a high quality camera with good lighting.

Then, after applying your settings run batchimg2img on our source content. It's a good idea to specify an output folder in case you want to do multiple render passes with different techniques. I have a pattern I like to use which varies from project to project, but an example may look like this:

`/out-1-1920x1080-sequence-details`
`/<folderBaseName>-<run>-<outputResoluton>-<primarySubject>-<notes>`

where `out` is the base of the folder name, `1` is the run, `1920x1080` is the output resolution, `sequence` is the main clip subject, and `details` are subtle changes between runs. This makes it easy for me to keep track of what is where when I am working on large projects.

## Step 5: Review image outputs (advanced)
In the end, my goal is not to have to delete frames or rerun them, or \**gasp*\* touch them up in photoshop. However sometimes this step is good to take and will improve the quality of your output if it's not to par with your expectations. Part of why I recommend larger outputs is because it requires less or no cleaning compared to smaller outputs, which tend to be messier or more random, or have more extreme lighting changes.

Cleanup methods:
1. Sometimes intermediate frames are janky and you must delete them manually after review. For example, a hand may be on a hip and jump to the chest and then back to the hip. Someone's mouth may pop open when it should be closed. This is normal. If it's just a frame here and there, and your output FPS is close to your input FPS it's pretty safe to delete the occasional unneeded frame. However if there are many frames in a row messed up, you may need to re-render them.

2. Re-run training again and again if your not happy. Ideally, you will modify your prompt slightly but keep all other settings the same. To save time, only re-run frames you need to.   
    - For example If you have 100 frames, and only need to reprocess frame 50 to frame 75, copy these frame to a new folder to save time on the reprocessing. Always process new frames and changes into a new output folder to prevent accidentally overwriting your changes.

3. Photoshop - I think this should be avoided at all costs. It's really only good for cleaning up a frame here and there. However not a very good idea for cleaning up multiple frames because it is time consuming, error prone, and does not scale.

## Step 6: Interpolation and final rendering
Interpolate with Flow Frames or with Google interpolate. They have different options and create different outputs. Flow Frame is great for long sequences of images and it's what I prefer to use generally. 

### Flow Frames
https://nmkd.itch.io/flowframes

Flow frame settings:
I use NVIDIA Interpolation AI - RIFE/CUDA

Output FPS - Recommend 6, 8, or 12. You may need to play with this, but try to match your input frame rate in the end.
This will translate to 12, 16, or 24 output FPS at Normal Speed

Output model is RIFE 4.0
Output mode is MP4.
<center>
<p>
        <img src="documentation/images/0003.gif">
</p>
</center>

### Google Interpolation
Google interpolate is great for creating transitions between two like images with different poses. Extreme differences in poses do not work well.

Simply pick two like frames and interpolate them here:
https://replicate.com/google-research/frame-interpolation

Google settings: 
6 Steps I have found to be ideal. However you should experiment!
<center>
<p style="width: 40%">
        <img src="documentation/images/0002.gif">
</p>
</center>

## Step 6: Compression for Web delivery and free video editing
I use EZGif for a lot of things. If you use it right, it's basically a great clip editor and compression tool with a low learning curve.

Use EZGif to generate final gif file, and optimize for web delivery. 
https://ezgif.com/maker