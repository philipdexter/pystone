import sys
import re
import click
import copy

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

my_deck = {
    'Humility': 1,
    'Equality': 2,
    'Doomsayer': 1,
    'Sunfury Protector': 2,
    'Wild Pyromancer': 2,
    'Aldor Peacekeeper': 2,
    'Big Game Hunter': 1,
    'Truesilver Champion': 2,
    'Consecration': 2,
    'Defender of Argus': 1,
    'Piloted Shredder': 2,
    'Holy Wrath': 2,
    'Antique Healbot': 1,
    'Sludge Belcher': 2,
    'Emperor Thaurissan': 1,
    'Sylvanas Windrunner': 1,
    'Dr. Boom': 1,
    'Lay on Hands': 1,
    'Tirion Fordring': 1,
    'Molten Giant': 2,
}

my_current_deck = copy.copy(my_deck)

def determine_color(card):
    if my_deck[card] == my_current_deck[card]:
        return OKGREEN
    elif my_deck[card] == 2 and my_current_deck[card] == 1:
        return OKBLUE
    else:
        return FAIL

def draw(c):
    global my_current_deck
    if c in my_current_deck:
        my_current_deck[c] -= 1

def put_back(c):
    global my_current_deck
    if c in my_current_deck:
        my_current_deck[c] += 1
    else:
        my_current_deck[c] = 1

def loop(f):
    while True:
        line = f.readline().strip()
        if not line:
            continue
        r = re.compile(r'^\[Zone\].*TRANSITIONING.*name=(.*)id.*zone=(HAND|DECK).*player=(.*)].*to FRIENDLY (PLAY|DECK)')
        m = r.match(line)
        if m:
            card = m.group(1).strip()
            action = m.group(2).strip()
            player = m.group(3).strip()
            yield (player, card, action)
        else:
            r = re.compile(r'^\[Zone\].*TRANSITIONING.*zone=PLAY.*player=(.*)].*to FRIENDLY PLAY \(Hero\)')
            m = r.match(line)
            if m:
                player = m.group(1)
                yield (player, 'HERO', '')

@click.group()
@click.argument('logfile', type=click.Path(exists=True))
@click.pass_context
def cli(ctx, logfile):
    ctx.obj['logfile'] = logfile

@click.command(help='Start the main deck tracker')
@click.pass_context
def track(ctx):
    me = '1'
    with open(ctx.obj['logfile'], 'r') as f:
        print(HEADER+'--------\nleft in deck'+ENDC+':\n{}'.format('\n'.join([(determine_color(card)+'{}: {}'+ENDC).format(card, count) for card,count in sorted(my_current_deck.items(), key=lambda x: x[0])])))
        for p, c, a in loop(f):
            if c == 'HERO':
                me = p
                continue
            if p == me:
                if a == 'HAND':
                    print('msg: putting {} into HAND'.format(c))
                    draw(c)
                elif a == 'DECK':
                    print('msg: putting {} into DECK'.format(c))
                    put_back(c)
            print(HEADER+'--------\nleft in deck'+ENDC+':\n{}'.format('\n'.join([(determine_color(card)+'{}: {}'+ENDC).format(card, count) for card,count in sorted(my_current_deck.items(), key=lambda x: x[0])])))

@click.command(help='Clear the hearthstone log file')
@click.pass_context
def clear(ctx):
    with open(ctx.obj['logfile'], 'w') as f:
        f.write('')
    print('log file cleared')

cli.add_command(track)
cli.add_command(clear)

if __name__ == '__main__':
    cli(obj={})
