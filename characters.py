
AI_LIST = [
    {
        "name": "Maisy",
        "rank": "1",
        "strategy": "random",  # options: "random", "negamax"
        "lookahead": 0,  # 1 to 6
        "error_rate": 1.00,  # 0.0 to 1.0; odds of making mistake
        "fitness": "greed", # options: greed, caution, balance
        "desc": "This 4 year old likes to move seeds.",
        "tagline": "Play is largely random. Very easy to win."
    },
    {
        "name": "Billy",
        "rank": "2",
        "strategy": "negamax",  # options: "random", "negamax"
        "lookahead": 1,  # 1 to 6
        "error_rate": 0.20,  # 0.0 to 1.0; odds of making mistake
        "fitness": "balance", # options: greed, caution, balance
        "desc": "Billy just learned the rules of the game.",
        "tagline": "Sometimes makes obviously bad moves. Still easy to win against."
    },
    {
        "name": "Emily",
        "rank": "3",
        "strategy": "negamax",  # options: "random", "negamax"
        "lookahead": 1,  # 1 to 6
        "error_rate": 0.05,  # 0.0 to 1.0; odds of making mistake
        "fitness": "balance", # options: greed, caution, balance
        "desc": "Emily is still a novice, but has played multiple times.",
        "tagline": "Blunt errors are rare, but still easy to win against."
    },
    {
        "name": "Jacob",
        "rank": "4",
        "strategy": "negamax",  # options: "random", "negamax"
        "lookahead": 2,  # 1 to 6
        "error_rate": 0.02,  # 0.0 to 1.0; odds of making mistake
        "fitness": "balance", # options: greed, caution, balance
        "desc": "Jacob plays on occasion with friends.",
        "tagline": "Jacob plays okay. Moderate difficulty."
    },
    {
        "name": "Emma",
        "rank": "5",
        "strategy": "negamax",  # options: "random", "negamax"
        "lookahead": 3,  # 1 to 6
        "error_rate": 0.00,  # 0.0 to 1.0; odds of making mistake
        "fitness": "greed", # options: greed, caution, balance
        "desc": "Emma is determined to win, even if she does not play much.",
        "tagline": "Emma is a gambler trying to win big. Moderate difficulty."
    },
    {
        "name": "Matthew",
        "rank": "6",
        "strategy": "negamax",  # options: "random", "negamax"
        "lookahead": 3,  # 1 to 6
        "error_rate": 0.00,  # 0.0 to 1.0; odds of making mistake
        "fitness": "caution", # options: greed, caution, balance
        "desc": "Matthew plays with friends and family, but is embarrased if he loses by too much.",
        "tagline": "Matthew is obsessed with keeping you from getting seeds, even if that makes the game long. Moderate difficulty."
    },
    {
        "name": "Olivia",
        "rank": "7",
        "strategy": "negamax",  # options: "random", "negamax"
        "lookahead": 4,  # 1 to 6
        "error_rate": 0.00,  # 0.0 to 1.0; odds of making mistake
        "fitness": "balance", # options: greed, caution, balance
        "desc": "Olivia plays regularly but doesn't consider hergreed a gamer.",
        "tagline": "A well-rounded player. Moderate/High difficulty."
    },
    {
        "name": "William",
        "rank": "8",
        "strategy": "negamax",  # options: "random", "negamax"
        "lookahead": 4,  # 1 to 6
        "error_rate": 0.03,  # 0.0 to 1.0; odds of making mistake
        "fitness": "greed", # options: greed, caution, balance
        "desc": "William loves to gamble and win big.",
        "tagline": "Smart but concentrates on his own store too much. Moderate/High difficulty."
    },
    {
        "name": "Sam",
        "rank": "9",
        "strategy": "negamax",  # options: "random", "negamax"
        "lookahead": 5,  # 1 to 6
        "error_rate": 0.03,  # 0.0 to 1.0; odds of making mistake
        "fitness": "caution", # options: greed, caution, balance
        "desc": "Sam plays a good game.",
        "tagline": "Too cautious, but a solid player. High difficulty."
    },
    {
        "name": "Sandra",
        "rank": "10",
        "strategy": "negamax",  # options: "random", "negamax"
        "lookahead": 6,  # 1 to 6
        "error_rate": 0.01,  # 0.0 to 1.0; odds of making mistake
        "fitness": "balance", # options: greed, caution, balance
        "desc": "Sandra is very good. Plays regularly.",
        "tagline": "High difficulty. error_rate very rare."
    },
    {
        "name": "R3 UNIT",
        "rank": "11",
        "strategy": "negamax",  # options: "random", "negamax"
        "lookahead": 6,  # 1 to 6
        "error_rate": 0.00,  # 0.0 to 1.0; odds of making mistake
        "fitness": "greed", # options: greed, caution, balance
        "desc": "An arrogant artificial intelligence.",
        "tagline": "Looks ahead 6 moves, but basically good. High difficulty."
    },
    {
        "name": "ThoughtNet",
        "rank": "12",
        "strategy": "negamax",  # options: "random", "negamax"
        "lookahead": 7,  # 1 to 6
        "error_rate": 0.00,  # 0.0 to 1.0; odds of making mistake
        "fitness": "greed", # options: greed, caution, balance
        "desc": "A deep artificial intelligence. ThoughtNet finds interacting with humans pleasing.",
        "tagline": "Very high difficulty. Still possible to win if you go first."
    },
]