import random

def main(input):
  # Version 1.0.1
  # Updated 10/28/25 22:36 PST
  
  # Get and normalize the character class
  char_class = input.get('class', 'Warrior').lower()

  # Default stat ranges per class
  ranges = {
    'warrior': {
      'atk': (10, 14),
      'def': (8, 12),
      'spd': (4, 6),
      'luck': (2, 5),
      'hp': (95, 105)
    },
    'rogue': {
      'atk': (8, 12),
      'def': (6, 10),
      'spd': (6, 8),
      'luck': (3, 6),
      'hp': (75, 85)
    },
    'skeleton': {
      'atk': (7, 10),
      'def': (4, 7),
      'spd': (5, 9),
      'luck': (5, 9),
      'hp': (65, 80)
    }
  }

  # Get class ranges or fallback to warrior if invalid
  class_ranges = ranges.get(char_class, ranges['warrior'])

  # Roll each stat within its range
  atk = random.randint(*class_ranges['atk'])
  deff = random.randint(*class_ranges['def'])
  spd = random.randint(*class_ranges['spd'])
  luck = random.randint(*class_ranges['luck'])
  hp = random.randint(*class_ranges['hp'])

  # Return the rolled stats
  return {
    'class': char_class.capitalize(),
    'atk': atk,
    'def': deff,
    'spd': spd,
    'luck': luck,
    'hp': hp
  }
