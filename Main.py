import pygame, neat, pickle, os,time
import sys
from Track import Track
from Car import Car
from gamelogic import *
import Visualize
#rendering handling for pygame
def Draw(cars):
    screen.fill(pygame.Color(0,0,0))
    screen.blit(trackSurface, (0,0))
    for car in cars:
        screen.blit(car.surf, car.rect)
        #for i in range(len(car.collisions)):
         #   pygame.draw.line(screen, pygame.Color(128, 128, 128), car.rect.center, car.collisions[i], 2)


#generates a new track
def NewTrack():
    valtr = Track(20, screenSize)
    pygame.draw.polygon(trackSurface, WHITE, valtr.getOuterBound())
    pygame.draw.polygon(trackSurface, Black, valtr.getInnerBound())
    return valtr
#loads configuration and creates population
def run(config_file):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)
    p = neat.Population(config)
    #p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-7')
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(2))
    winner = p.run(eval_genomes, 200)
# The actual game runs in here
def eval_genomes(genomes,config):
    start = time.time()
    trackSurface.fill(pygame.Color(0, 0, 0))
    valtr = NewTrack()
    #print(valtr.edges)
    valtr.surf = trackSurface
    valtr.rect = trackSurfaceRect
    valtr.surf.set_colorkey(pygame.Color(0, 0, 0))
    valtr.hitmask = get_colorkey_hitmask(valtr.surf, valtr.rect)
    averageX = (valtr.getOuterBound()[0][0]+valtr.getInnerBound()[0][0])/2
    averageY = (valtr.getOuterBound()[0][1]+valtr.getInnerBound()[0][1])/2
    alignmentVec = (valtr.getInnerBound()[0][0]-valtr.getInnerBound()[1][0],valtr.getInnerBound()[0][1]-valtr.getInnerBound()[1][1])
    cordinates = (averageX, averageY)
    cars = []
    nets = []
    ge = []
    #creats nets and assigns them a car object
    for _,g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0.00
        ge.append(g)
        car = Car(cordinates, alignmentVec) # places the car in a valid place on the track
        car.hitmask = get_alpha_hitmask(car.surf,car.rect)
        cars.append(car)
    while 1:
        clock.tick(30)
        Draw(cars)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_p:Visualize.draw_net(config, max(ge, key=lambda g: g.fitness), True) # draws Net with current best fitness when key P is pressed
        if len(cars) == 0 or (time.time()-start)>100 or pygame.key.get_pressed()[pygame.K_c]: #terminates round when key c is pressed
            break
        for i,car in enumerate(cars):
            car.move()
            car.hitmask = get_alpha_hitmask(car.surf, car.rect)
            directions = [car.acceleration.normalize(),car.acceleration.normalize().rotate(90),car.acceleration.normalize().rotate(270),car.acceleration.normalize().rotate(45),car.acceleration.normalize().rotate(135),car.acceleration.normalize().rotate(225),car.acceleration.normalize().rotate(315)]
            car.collisions = list()
            car.distances = list()
            for s in range(len(directions)):
                point,distance = car.DetectEdges(valtr, directions[s])
                car.collisions.append(point)
                car.distances.append(distance)
            output = nets[i].activate(tuple(car.distances))
            if output[0]>0:ge[i].fitness += 0.1
            car.motion = abs(output[0])
            car.angleSpeed = 3 * output[1]
            ge[i].fitness += 0.001
            if car.velocity.magnitude()<5:
                ge[i].fitness -= 0.1
            else:
                ge[i].fitness += car.velocity.magnitude()
            # removes net car and genome if collides with edge or fitness is too small
            if PixelPerfectCollision(car, valtr) or ge[i].fitness < -10:
                cars.pop(i)
                nets.pop(i)
                ge.pop(i)

if __name__ == '__main__':
    screenSize = 1000, 800
    clock = pygame.time.Clock()
    trackSurface = pygame.Surface(screenSize)
    debugSurf = pygame.Surface(screenSize)
    debugSurf.set_colorkey(pygame.Color(0, 0, 0))
    trackSurfaceRect = trackSurface.get_rect()
    Black = pygame.Color(0,0,0)
    WHITE = pygame.Color(255,255,255)
    screen = pygame.display.set_mode(screenSize)
    pygame.init()
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)