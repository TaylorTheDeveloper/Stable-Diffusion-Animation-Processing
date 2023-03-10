
# Stable Diffusion Animation Processing

<center>
    <p style="width: 60%">          
            <img src="documentation/images/paintingAnimation/002-1080-header.gif">
            <img src="documentation/images/readme/composited.gif">
    </p>
</center>

- [Stable Diffusion Animation Processing](#stable-diffusion-animation-processing)
- [Contact](#contact)
- [General Animation Processing Steps](#general-animation-processing-steps)
  - [Step 1: Find or create a good input video](#step-1-find-or-create-a-good-input-video)
  - [Step 2: Background Extraction (Optional but recommended)](#step-2-background-extraction-optional-but-recommended)
  - [Step 3: Frame Extraction](#step-3-frame-extraction)
  - [Step 4: Stable Diffusion](#step-4-stable-diffusion)
  - [Step 5: Review image outputs (advanced)](#step-5-review-image-outputs-advanced)
  - [Step 6: Rendering](#step-6-rendering)
    - [Professional Video Rendering Software](#professional-video-rendering-software)
    - [Interpolation](#interpolation)
      - [*Interpolation with Flow Frames*](#interpolation-with-flow-frames)
      - [*Interpolation with Google's Frame Interpolation*](#interpolation-with-googles-frame-interpolation)
  - [Step 7: Compression for Web delivery and free video editing](#step-7-compression-for-web-delivery-and-free-video-editing)
- [Dealing with Long Video Sequences](#dealing-with-long-video-sequences)
  - [Frame Reduction](#frame-reduction)
  - [Folder Generation and scene separation](#folder-generation-and-scene-separation)
  - [Output for long sequences and rendering times](#output-for-long-sequences-and-rendering-times)
- [Notes](#notes)

This is my workflow for generating beautiful, semi-temporally-coherent videos using stable diffusion and a few other tools. More example outputs can be found in the [prompts subfolder](https://github.com/TaylorTheDeveloper/Stable-Diffusion-Animation-Processing/blob/main/prompts/paintingAnimation/prompt.EXAMPLES.md)

My goal is to help speed up the adoption of this technology and improve its viability for professional use and commercial applications across filmmaking, marketing, and more. I believe that these tools should be open source and publicly available and encourage others to do the same.

There are limitations due to the nature of the diffusion process- outputs tend to favor randomness. This makes for fantastic still artwork- but animations are challenging. I've tried to make this guide as user friendly as possible, however expect to set up and configure a few things! You can get in touch with me below or through PRs here if you have questions.

PRs will be reviewed- so if you develop cool prompts please share them here! This page and guide will only be updated with well vetted process changes, so please be prepared for that!

A big thank you to the AI community, AI researchers who've spent years developing these and other AI models, and the netizens who have been contributing and sharing their learning with each other online. This repo is dedicated to all of you and your contributions. 

# Contact 

- You can find me on discord here: TemporalCoherence#2744
- I hang out in the animation group here: https://discord.gg/stablediffusion

# General Animation Processing Steps

## Step 1: Find or create a good input video
1. Avoid videos where the focus is changing or going in and out.
2. Avoid videos with terrible lighting or a lot of noise.
3. Movement and motion is ok, but very fast blurry movement will increase randomness of output and should be avoided.
4. Recommend MP4 or WebM videos. I have also worked with MTS format, but it's less popular.
5. Make sure to get these video details for use later: Video height and width (Step 3), and FPS (Step 2)

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

FFMpeg command for 24 FPS: `ffmpeg -r 24 raw/%08d.png -i input.mp4`

If you're dealing with a video with multiple scenes, please see the [section below](#dealing-with-long-video-sequences) for large videos.

## Step 4: Stable Diffusion 
1. Make sure your using Stable Diffusion Web UI! https://github.com/AUTOMATIC1111/stable-diffusion-webui
    - [Getting started Guide for Automatic1111](https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/Install-and-Run-on-NVidia-GPUs)
2. See Prompts/core.prompt for specific details on settings that I used for Stable Diffusion. 
    - As I create more prompt configurations, I will upload them here! If you have some to share, I will accept pull requests!
    - While not expressly required, I like to make sure the source width/height and output width/hight are the same. If you want to match outputs closely, aspect ratio should be the same or close. 
       - An aside: With content on the web, quality and bit rate/depth varies widely. So if videos are lower quality I generally will render them out with increased heights and widths. If 240x320 video then make sure the settings match or are higher, for example I may got with 480x640 or even 960x1280.For 1920x1080, however, I generally keep it the same. This rule may not apply to you if you use a high quality camera with good lighting.

Then, after applying your settings run batchimg2img on our source content. It's a good idea to specify an output folder in case you want to do multiple render passes with different techniques. I have a pattern I like to use which varies from project to project, but an example may look like this:

Template:
`/<folderBaseName>-<primarySubject>-<run>-<outputResoluton>-<notes>`

Example:
`/out-sequenceA-001-1920x1080-Model-Anime-EulerA-CGF17.5-noise0.7`

Some real folders I used on a recent project testing different things [for a large project](#dealing-with-long-video-sequences) . 

`/out-selectedstills_540p_mod-anime_noise-0.7`

`/out-selectedstills_540p_mod-anime_noise-0.3`

`/out-selectedstills_540p_mod-protogen_noise-0.3`

`out` is the base of the folder name I use for all output sequences. My input folders are usually prefixed with `raw`. `540p` is the output resolution (960x540), `selectedstills` is the main clip subject, and `details` are subtle changes between runs, in the case above model and noise adjustments- but it can be any values you want to track. This makes it easy for me to keep track of what is where when I am working on large projects.

## Step 5: Review image outputs (advanced)
In the end, my goal is not to have to delete frames or rerun them, or \**gasp*\* touch them up in photoshop. However sometimes this step is good to take and will improve the quality of your output if it's not to par with your expectations. Part of why I recommend larger outputs is because it requires less or no cleaning compared to smaller outputs, which tend to be messier or more random, or have more extreme lighting changes.

Cleanup methods:
1. Sometimes intermediate frames are janky and you must delete them manually after review. For example, a hand may be on a hip and jump to the chest and then back to the hip. Someone's mouth may pop open when it should be closed. This is normal. If it's just a frame here and there, and your output FPS is close to your input FPS it's pretty safe to delete the occasional unneeded frame. However if there are many frames in a row messed up, you may need to re-render them.

2. Re-run training again and again if your not happy. Ideally, you will modify your prompt slightly but keep all other settings the same. To save time, only re-run frames you need to.   
    - For example If you have 100 frames, and only need to reprocess frame 50 to frame 75, copy these frame to a new folder to save time on the reprocessing. Always process new frames and changes into a new output folder to prevent accidentally overwriting your changes.

3. Photoshop - I think this should be avoided at all costs. It's really only good for cleaning up a frame here and there. However not a very good idea for cleaning up multiple frames because it is time consuming, error prone, and does not scale.

## Step 6: Rendering

### Professional Video Rendering Software

Using an application like Adobe Premiere, After Effects, of Davinci Resolve to create your image sequence and render it into a video.

### Interpolation
Interpolate with Flow Frames or with Google interpolate. They have different options and create different outputs. Flow Frame is great for long sequences of images and it's what I prefer to use generally.

#### *Interpolation with Flow Frames*
https://nmkd.itch.io/flowframes

Flow frame settings:
I use NVIDIA Interpolation AI - RIFE/CUDA
Make sure your output FPS matches the original FPS of your video!

<center>
<p>
        <img src="documentation/images/paintingAnimation/0003.gif">
</p>
</center>

#### *Interpolation with Google's Frame Interpolation*
Google interpolate is great for creating transitions between two like images with different poses. Extreme differences in poses do not work well.

Simply pick two like frames and interpolate them here:
https://replicate.com/google-research/frame-interpolation

Google settings: 
6 Steps I have found to be ideal. However you should experiment!
<center>
<p style="width: 40%">
        <img src="documentation/images/paintingAnimation/0002.gif">
</p>
</center>

## Step 7: Compression for Web delivery and free video editing
I use EZGif for a lot of things. If you use it right, it's basically a great clip editor and compression tool with a low learning curve.

Use EZGif to generate final gif file, and optimize for web delivery. 
https://ezgif.com/maker

# Dealing with Long Video Sequences

## Frame Reduction
So, let's say your dealing with a thousand frames, or perhaps ten thousand, or even a million. This is often the case if you processing an existing music video, film, or just a long sequence of video.

It makes little sense to do this without having some preview of the output because it takes a long time to complete. That's where `/tools/frameReducer.py` comes in. Frame reducer takes an input directory of stills and and output directory, and copies over every 2nd frame. You can make this every 3rd, 4th, 5th, 100th, 150th frame if you wish by specifying the `-n` parameter. For large files with multiple scenes, I will set it to 100-210th frame to grab a still every five seconds or so. I can then reduce my number of frames by a factor of 210 (or whatever `n` is) and quickly preview a larger clips output. 

Using this, I am able to sample the source images from my long sequence and extract a handful of key frames so I could preview the outputs quickly.

<center>
    <p style="width: 80%">          
            <img src="documentation/images/readme/5000items.PNG">
    </p>
    <p style="width: 80%">          
            <img src="documentation/images/readme/28items.PNG">
    </p>
</center>


Some examples of usage:

- Skip every other frame (default)

`python frameReducer.py-src .\raw_arcade\ -dest .\selected_arcade\  `

- Skip every 4th frame

`python frameReducer.py-src .\raw_arcade\ -dest .\selected_arcade\ -n 4 `

- Skip every 150th frame

`python frameReducer.py-src .\raw_arcade\ -dest .\selected_arcade\ -n 150`

## Folder Generation and scene separation

When dealing with multiple scenes I put each scene into a subfolder. This makes it easy to rerun select scenes If I need to. It lets me queue things up for interpolation easier. Additionally, it's very organized and I can find things quickly. I use `/tools/folderGenerator.py` to do this for me. It takes a `-start` and a `-stop` parameter, which are positive integers like 1 and 10, which are the range of folders you wish to create. 
<center>
    <p style="width: 80%">          
            <img src="documentation/images/readme/manyfolders.PNG">
    </p>
</center>


## Output for long sequences and rendering times

I generally keep my inputs 540p and higher. On my RTX2070, it usually takes less than 5 seconds to render a single frame at 540p. 

For some select sequences, I opt for 1080p which generally matches my input footage width/heigh and produces better far better results, however it takes 45 seconds per frame- which is almost ten times longer. This time investment makes [frameReduction](#frame-reduction) a critical part of the process!

# Notes

Using inputs that are 1080p.

Working with paintingAnimation promp I am able to reduce image generation time from ~45 sec to ~4.5 sec by doing 540p instead of 1080p. However image is far more random. Going down to 720 is better and less random and 1080p. It takes about ~9 sec per frame and is more accurate than 540p. It still doesn't compare to 1080p.

Found that reducing steps from 28 to 14 seems to do a good job and image quality is very close to the same. It reduces time by about 50%r. However I only recommend doing this for background footage, as the accuracy and clarity of 28 steps is FAR better than 14 steps.

Assuming 100 frames of video (about ~4 seconds of video at 24 FPS)

1080p 28 steps: (45x100)/60 = 75 minute render time

720p 28 steps: (9x100)/60 = 15 minute render time

540p 28 steps: (4.5x100)/60 = 7.5 minute render time


1080p 14 steps: (22.5x100)/60 = 37.5 minute render time

720p 14 steps: (4.5x100)/60 = 7.5 minute render time

540p 14 steps: (2.2x100)/60 = 3.6 minute render time