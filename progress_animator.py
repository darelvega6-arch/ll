import asyncio
import time

class ProgressAnimator:
    def __init__(self):
        self.animations = {
            'extracting': ['🎬', '🎥', '🎞️', '📹', '🎦'],
            'separating': ['🎵', '🎶', '🎼', '🎹', '🎸'],
            'detecting': ['👤', '👥', '👨', '👩', '🧑'],
            'transcribing': ['🎤', '🎙️', '📢', '📣', '🔊'],
            'translating': ['🌍', '🌎', '🌏', '🗺️', '🌐'],
            'cloning': ['🎭', '🎪', '🎨', '✨', '⭐'],
            'mixing': ['🎚️', '🎛️', '🔊', '📻', '🎧'],
            'finalizing': ['🎬', '🎉', '✅', '🎊', '🏆']
        }
        
        self.progress_bars = {
            0: '▱▱▱▱▱▱▱▱▱▱',
            10: '▰▱▱▱▱▱▱▱▱▱',
            20: '▰▰▱▱▱▱▱▱▱▱',
            30: '▰▰▰▱▱▱▱▱▱▱',
            40: '▰▰▰▰▱▱▱▱▱▱',
            50: '▰▰▰▰▰▱▱▱▱▱',
            60: '▰▰▰▰▰▰▱▱▱▱',
            70: '▰▰▰▰▰▰▰▱▱▱',
            80: '▰▰▰▰▰▰▰▰▱▱',
            90: '▰▰▰▰▰▰▰▰▰▱',
            100: '▰▰▰▰▰▰▰▰▰▰'
        }
    
    def get_progress_bar(self, percentage):
        """Obtiene la barra de progreso visual"""
        rounded = (percentage // 10) * 10
        return self.progress_bars.get(rounded, self.progress_bars[0])
    
    def get_animation_frame(self, stage, frame_index):
        """Obtiene el frame de animación actual"""
        frames = self.animations.get(stage, ['⏳'])
        return frames[frame_index % len(frames)]
    
    def format_progress_message(self, stage, stage_name, percentage, details=""):
        """Formatea el mensaje de progreso con animación"""
        icon = self.get_animation_frame(stage, int(time.time() * 2) % 5)
        bar = self.get_progress_bar(percentage)
        
        message = f"{icon} *{stage_name}*\n"
        message += f"{bar} {percentage}%\n"
        
        if details:
            message += f"\n💡 {details}"
        
        return message
    
    async def animate_progress(self, message_obj, stage, stage_name, duration=3):
        """Anima el progreso durante una etapa"""
        steps = 10
        for i in range(steps + 1):
            percentage = int((i / steps) * 100)
            text = self.format_progress_message(stage, stage_name, percentage)
            
            try:
                await message_obj.edit_text(text, parse_mode='Markdown')
            except:
                pass
            
            if i < steps:
                await asyncio.sleep(duration / steps)
