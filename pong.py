import pygame, sys, random
import pongInit as init

pygame.mixer.pre_init(44100, -16, 2, 512) # Last number should be changed to reduce sound delay
pygame.init()  # Initializes pygame modules, always needed
pygame.font.init()
clock = pygame.time.Clock()


def update_screen():
    screen.fill(init.bg_color)
    pygame.draw.ellipse(screen, init.light_grey, ball)
    pygame.draw.rect(screen, init.light_grey, l_paddle)
    pygame.draw.rect(screen, init.light_grey, r_paddle)
    pygame.draw.rect(screen, init.light_grey, centre_line)

    l_score_text = init.score_font.render(f"{init.l_score}", False, init.light_grey)
    screen.blit(l_score_text, (init.l_score_x, init.l_score_y))

    r_score_text = init.score_font.render(f"{init.r_score}", False, init.light_grey)
    screen.blit(r_score_text, (init.r_score_x, init.r_score_y))

def ball_move():
    # Ball and wall collisions
    if ball.top <= 0 or ball.bottom >= init.screen_height:
        init.ball_speed_y *= -1
        pygame.mixer.Sound.play(init.pong_sound)
    if ball.left <= 0 or ball.right >= init.screen_width:
        pygame.mixer.Sound.play(init.score_sound)
        # Update score
        if ball.left <= 0:
            init.l_score += 1
        else:
            init.r_score += 1

        # Reset ball
        ball.center = (init.screen_width/2, init.screen_height/2)

        init.ball_speed_x = ((init.ball_speed_x / abs(init.ball_speed_x)) * 5) * -1 # reset ball speed to 5 and change direction
        init.ball_speed_y = random.choice((-5, 5))
        init.speed_up_num = 10000

    # Ball and player collisions
    if ball.colliderect(l_paddle):
        pygame.mixer.Sound.play(init.pong_sound)
        if abs(ball.left - l_paddle.right) < 10: # collision between paddle and ball
            init.ball_speed_x *= -1
        elif abs(ball.top - l_paddle.bottom) < 10: # ball and bottem of paddle
            init.ball_speed_y *= -1
        elif abs(ball.bottom - l_paddle.top) < 10: # ball and top of paddle
            init.ball_speed_y *= -1

    if ball.colliderect(r_paddle):
        pygame.mixer.Sound.play(init.pong_sound)
        if abs(ball.right - r_paddle.left) < 10: # collision between paddle and ball
            init.ball_speed_x *= -1
        elif abs(ball.top - r_paddle.bottom) < 10: # ball and bottem of paddle
            init.ball_speed_y *= -1
        elif abs(ball.bottom - r_paddle.top) < 10: # ball and top of paddle
            init.ball_speed_y *= -1

    # Change x and y of ball object not ones in init file
    ball.x += init.ball_speed_x
    ball.y += init.ball_speed_y

def paddle_move():
    if l_paddle.top + init.l_player_speed > 0 and l_paddle.bottom + init.l_player_speed < init.screen_height:
        l_paddle.y += init.l_player_speed
    if r_paddle.top + init.r_player_speed > 0 and r_paddle.bottom + init.r_player_speed < init.screen_height:
        r_paddle.y += init.r_player_speed

def handle_inputs():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


        # Moving player
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                init.r_player_speed -= 7
            if event.key == pygame.K_DOWN:
                init.r_player_speed += 7
            if event.key == pygame.K_w:
                init.l_player_speed -= 7
            if event.key == pygame.K_s:
                init.l_player_speed += 7
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                init.r_player_speed += 7
            if event.key == pygame.K_DOWN:
                init.r_player_speed -= 7
            if event.key == pygame.K_w:
                init.l_player_speed += 7
            if event.key == pygame.K_s:
                init.l_player_speed -= 7

def check_game_over():
    if init.l_score == init.game_over_score:
        init.display_game_over = True
        init.winning_player = "LEFT"
        pygame.mixer.Sound.play(init.win_sound)

    elif init.r_score == init.game_over_score:
        init.display_game_over = True
        init.winning_player = "RIGHT"
        pygame.mixer.Sound.play(init.win_sound)

def display_game_over_screen():
    screen.fill(init.bg_color)

    l_score_text = init.score_font.render(f"{init.l_score}", False, init.light_grey)
    screen.blit(l_score_text, (init.l_score_x, init.l_score_y))

    r_score_text = init.score_font.render(f"{init.r_score}", False, init.light_grey)
    screen.blit(r_score_text, (init.r_score_x, init.r_score_y))

    pygame.draw.rect(screen, init.light_grey, centre_line)

    text1 = init.text_font.render("GAME OVER", False, init.light_grey)
    screen.blit(text1, (init.GO1_x, init.GO1_y))


# Screen
screen = pygame.display.set_mode((init.screen_width, init.screen_height))
pygame.display.set_caption("Pong")

# Objects
ball = pygame.Rect(init.ball_x, init.ball_y, init.ball_size, init.ball_size)
l_paddle = pygame.Rect(init.l_paddle_x, init.l_paddle_y, init.paddle_width, init.paddle_height)
r_paddle = pygame.Rect(init.r_paddle_x, init.r_paddle_y, init.paddle_width, init.paddle_height)
centre_line = pygame.Rect(init.line_x, init.line_y, init.line_width, init.line_height)

# Main Game Loop
while True:
    if init.display_game_over:
        display_game_over_screen()
        handle_inputs()

    else:
        handle_inputs()
        ball_move()
        paddle_move()
        update_screen()
        check_game_over()

    pygame.display.flip()
    clock.tick(60)  # Limits how fast loop runs

