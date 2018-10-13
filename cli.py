# -*- coding:utf8 -*-
"""
Cli.py provides command line interface for puzzle solver
"""
from argparse import ArgumentParser


class Cli:

    @staticmethod
    def create_parser():
        # create the main parser for CLI
        command_parser = ArgumentParser(prog="Puzzle Solver",
                                        description="Solve a x b puzzle using heuristic search")
        # create branches for DFS, BFS and A* Search
        method_parsers = command_parser.add_subparsers(help='[command] help',
                                                       dest="subparser_name")
        method_parsers.required = True
        # create a general template for searches
        template_parser = ArgumentParser(add_help=False,
                                         conflict_handler='resolve')
        template_parser.add_argument('-init',
                                     dest='init_state',
                                     metavar="0, 1, 2, 3 ...",
                                     action="store",
                                     help="Initial State",
                                     required=True)
        template_parser.add_argument('-goal',
                                     dest='goal_state',
                                     metavar="3, 2, 1, 0 ...",
                                     action="store",
                                     help="Goal State",
                                     required=True)
        template_parser.add_argument('-width',
                                     dest='width',
                                     metavar="int",
                                     action="store",
                                     help="Width of the puzzle",
                                     required=True)
        template_parser.add_argument('-height',
                                     dest='height',
                                     metavar="int",
                                     action="store",
                                     help="Height of the puzzle",
                                     required=True)
        # BFS command
        bfs_parser = method_parsers.add_parser('BFS',
                                               parents=[template_parser],
                                               help='Run BFS')
        bfs_parser.add_argument('-h1',
                                dest='h1',
                                action="store_const",
                                const=True,
                                default=False,
                                help="Enable Manhattan Heuristic Function")
        bfs_parser.add_argument('-h2',
                                dest='h2',
                                action="store_const",
                                const=True,
                                default=False,
                                help="Enable Permutation Heuristic Function")
        # A* command
        a_parser = method_parsers.add_parser('Astar',
                                               parents=[template_parser],
                                               help='Run A* algorithm')
        a_parser.add_argument('-h1',
                                dest='h1',
                                action="store_const",
                                const=True,
                                default=False,
                                help="Enable Manhattan Heuristic Function")
        a_parser.add_argument('-h2',
                                dest='h2',
                                action="store_const",
                                const=True,
                                default=False,
                                help="Enable Permutation Heuristic Function")
        # DFS
        dfs_parser = method_parsers.add_parser('DFS',
                                             parents=[template_parser],
                                             help='Run DFS')
        return command_parser
