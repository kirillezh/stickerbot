"""
This module contains the VideoConverter class for converting videos to different formats.
"""
import os
import logging
import subprocess

class VideoConverter:
    """Class for video conversion"""
    @staticmethod
    def convert_round(file: str) -> bool:
        """Convert video to round format"""
        try:
            subprocess.run([
                'ffmpeg','-hide_banner', '-loglevel', 'error', '-i', file, '-r', '30', '-t', '2.99', 
                '-filter_complex', 
                "[0:v]scale=512:512:force_original_aspect_ratio=decrease,crop=ih:ih[video square];[video square]split=3[black canvas][white canvas][video square];[black canvas]setsar=1:1,drawbox=color=black@1:t=fill[black background];[white canvas]scale=w=iw:h=iw,format=yuva444p,geq=lum='p(X,Y)':a='st(1,pow((W-10),2)/4)+st(3,pow(X-(W/2),2)+pow(Y-(H/2),2));if(lte(ld(3),ld(1)),255,0)',drawbox=color=white@1:t=fill[scaled up white circle];[scaled up white circle]scale=w=iw:h=iw[white circle];[black background][white circle]overlay[alpha mask];[video square][alpha mask]alphamerge,format=yuva420p",
                '-filter_complex_threads', '1', '-c:v', 'libvpx-vp9', 
                '-auto-alt-ref', '0', '-preset', 'ultrafast', '-an', 
                '-b:v', '400K', file.replace(".mp4", ".webm")],
                check=True)
            os.remove(file)
            return True
        except Exception as e:
            os.remove(file)
            logging.warning('Error at %s', 'division', exc_info=e)
            return False

    @staticmethod
    def convert_video(file: str) -> bool:
        """Convert video to video sticker format"""
        try:
            subprocess.run([
                'ffmpeg','-hide_banner', '-loglevel', 'error', '-y', '-i', file, '-r', '30', '-t', '2.99',           
                 '-an', '-c:v', 'libvpx-vp9','-pix_fmt', 'yuva420p' , '-vf', 'scale=512:512:force_original_aspect_ratio=decrease', '-b:v', '400K', file.replace(".mp4", ".webm")],
                check=True)
            os.remove(file)
            return True
        except Exception as e:
            os.remove(file)
            logging.warning('Error at %s', 'division', exc_info=e)
            return False 