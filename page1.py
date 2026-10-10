import sys
import os
import subprocess
import pygame

try:
    from moviepy.editor import VideoFileClip
except ImportError:
    from moviepy import VideoFileClip

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("OncoVue - Startup Stream")

# Define Theme Colors (RGB format for Pygame)
COLOR_ORCHID = (109, 40, 217)
COLOR_ROSE = (236, 72, 153)
COLOR_LAVENDER = (192, 132, 252)
COLOR_BLUSH = (249, 168, 212)
COLOR_FROST = (250, 247, 255)
COLOR_DEEP_AMETHYST = (46, 16, 101)

# Ensure path safety
video_path = os.path.join("assets", "startup.mp4")

if os.path.exists(video_path):
    clip = VideoFileClip(video_path).without_audio()
    fps = clip.fps
    clock = pygame.time.Clock()
    
    # Pre-render static theme UI overlay textures for performance
    try:
        font_logo = pygame.font.SysFont("georgia", 36, bold=True, italic=True)
        font_tagline = pygame.font.SysFont("arial", 12, bold=True)
    except:
        font_logo = pygame.font.Font(None, 40)
        font_tagline = pygame.font.Font(None, 16)
        
    logo_surf = font_logo.render("OncoVue", True, COLOR_ORCHID)
    tagline_surf = font_tagline.render("WE CARE TO CURE", True, COLOR_ROSE)
    
    # Calculate video bounds
    total_duration = clip.duration
    frame_count = 0
    estimated_total_frames = int(total_duration * fps)
    
    for frame in clip.iter_frames(fps=fps, dtype="uint8"):
        run_loop = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_loop = False
                break
        
        if not run_loop:
            break
            
        # Convert video frame array to pygame Surface
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
        frame_surface = pygame.transform.scale(frame_surface, (1280, 720))
        
        # Blit main video frame
        screen.blit(frame_surface, (0, 0))
        
        # --- Apply OncoVue Premium Theme Overlays ---
        # 1. Subtle Glassmorphic watermark backing card in top-left
        watermark_bg = pygame.Surface((240, 75), pygame.SRCALPHA)
        pygame.draw.rect(watermark_bg, (250, 247, 255, 180), (0, 0, 240, 75), border_radius=12)
        pygame.draw.rect(watermark_bg, (255, 255, 255, 120), (0, 0, 240, 75), width=1, border_radius=12)
        screen.blit(watermark_bg, (30, 30))
        
        # 2. Draw Text Overlays
        screen.blit(logo_surf, (45, 38))
        screen.blit(tagline_surf, (47, 78))
        
        # 3. Custom Horizontal Progress Indicator at the bottom
        frame_count += 1
        progress_ratio = min(frame_count / estimated_total_frames, 1.0)
        progress_width = int(1280 * progress_ratio)
        
        # Draw background track
        pygame.draw.rect(screen, (109, 40, 217, 50), (0, 714, 1280, 6))
        # Draw active Rose gradient progress bar line
        pygame.draw.rect(screen, COLOR_ROSE, (0, 714, progress_width, 6))
        # --------------------------------------------
        
        pygame.display.flip()
        clock.tick(fps)
        
    clip.close()
    
else:
    # --- High-End Fallback Biotech Visual Screen (Missing Video) ---
    fallback_clock = pygame.time.Clock()
    
    try:
        font_title = pygame.font.SysFont("georgia", 54, bold=True, italic=True)
        font_sub = pygame.font.SysFont("arial", 14, bold=True)
        font_status = pygame.font.SysFont("arial", 12)
    except:
        font_title = pygame.font.Font(None, 64)
        font_sub = pygame.font.Font(None, 20)
        font_status = pygame.font.Font(None, 16)
        
    title_text = font_title.render("OncoVue", True, COLOR_DEEP_AMETHYST)
    sub_text = font_sub.render("WE CARE TO CURE", True, COLOR_ROSE)
    status_text = font_status.render("INITIALIZING SECURE GRAPHICS SYSTEM...", True, COLOR_ORCHID)
    
    # Play static fallback state for 1.5 seconds (45 frames at 30 fps)
    for tick in range(45):
        # Allow exit events even inside fallback
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        # Draw Soft Pastel Background with a simulated radial glow
        screen.fill(COLOR_FROST)
        for r in range(400, 100, -10):
            alpha = int(45 * (1.0 - (r / 400.0)))
            glow_surf = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (249, 168, 212, alpha), (r, r), r)
            screen.blit(glow_surf, (640 - r, 360 - r))
            
        # Draw Glassmorphic Accent Box
        panel = pygame.Surface((600, 240), pygame.SRCALPHA)
        pygame.draw.rect(panel, (255, 255, 255, 140), (0, 0, 600, 240), border_radius=20)
        pygame.draw.rect(panel, (109, 40, 217, 30), (0, 0, 600, 240), width=1, border_radius=20)
        screen.blit(panel, (340, 240))
        
        # Center Branding UI Text on Fallback panel
        screen.blit(title_text, (640 - (title_text.get_width() // 2), 275))
        screen.blit(sub_text, (640 - (sub_text.get_width() // 2), 345))
        screen.blit(status_text, (640 - (status_text.get_width() // 2), 415))
        
        # Slim loader indicator bar inside fallback panel
        bar_width = int(400 * (tick / 45.0))
        pygame.draw.rect(screen, (109, 40, 217, 30), (440, 440, 400, 4), border_radius=2)
        pygame.draw.rect(screen, COLOR_ROSE, (440, 440, bar_width, 4), border_radius=2)
        
        pygame.display.flip()
        fallback_clock.tick(30)

# Graceful cleanup and forward progression
pygame.quit()
    
# Launch the fast loader first to cover the screen
subprocess.Popen([sys.executable, "loader.py"])
subprocess.Popen([sys.executable, "page2.py"])
sys.exit()