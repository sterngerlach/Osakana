# coding: utf-8
# ga.py

import copy
import numpy as np
import random

from automaton import FishAutomaton
from simulator import CompetitionSimulator

class GeneticAlgorithmSimulator(object):
    """
    遺伝的アルゴリズムによりオートマトンを進化させるためのクラス
    """
    
    def __init__(self):
        self.simulator = CompetitionSimulator()
    
    def gene_to_automaton(self, gene, name):
        automaton = FishAutomaton(name)
        automaton.states = { trans[0]: trans[1] for trans in gene }
        automaton.transitions = { trans[0]: { "g": trans[2], "w": trans[3] }
                                  for trans in gene }
        automaton.init_state = gene[0][0]
        automaton.current_state = gene[0][0]
        
        return automaton
    
    def evaluate(self, genes):
        automatons = [self.gene_to_automaton(gene, "") for gene in genes]
        num_of_wins, num_of_loses, num_of_draws, scores = \
            self.simulator.run_round_robin(automatons)
        return scores
    
    def selection(self, genes, norm_scores):
        return np.random.choice(np.arange(len(genes)), p=norm_scores)
    
    def crossover(self, gene0, gene1):
        new_gene0 = copy.deepcopy(gene0)
        new_gene1 = copy.deepcopy(gene1)
        state = random.randrange(len(gene0))
        new_gene0[state] = new_gene1[state]
        
        return new_gene0
    
    def mutation(self, gene):
        new_gene = copy.deepcopy(gene)
        
        if random.random() > 0.5:
            state = random.randrange(len(gene))
            new_state = random.randrange(len(gene)) + 1
            action = random.randrange(2)
            new_gene[state][action + 2] = new_state
        else:
            state = random.randrange(len(gene))
            new_action = "w" if random.random() > 0.5 else "g"
            new_gene[state][1] = new_action
        
        return new_gene
    
    def generate_random_gene(self, num_states):
        gene = [[i + 1, "w", 1, (i + 1) % num_states + 1] for i in range(num_states)]
        
        for i in range(num_states):
            if random.random() > 0.5:
                state = random.randrange(num_states)
                new_state = random.randrange(num_states) + 1
                action = random.randrange(2)
                gene[state][action + 2] = new_state
            else:
                state = random.randrange(num_states)
                new_action = "w" if random.random() > 0.5 else "g"
                gene[state][1] = new_action
    
        return gene
    
    def run(self):
        state_num = 3
        gene_num = 100
        max_generation = 100
        mutation_rate = 0.2
        crossover_rate = 0.4
        
        genes = [self.generate_random_gene(state_num) for i in range(gene_num)]
        new_genes = []
        
        best_score = 0
        best_gene = []
        best_automaton = None
        
        for gen in range(max_generation):
            scores = self.evaluate(genes)
            max_score = np.max(scores)
            
            print("run(): generation: {}, average: {}, best: {}"
                  .format(gen, np.round(np.average(scores), 1), best_score))
            
            if max_score > best_score:
                best_score = max_score
                best_gene = genes[np.argmax(scores)]
            
            scores = [i if i >= 100 else 100 for i in scores]
            norm_scores = [i / sum(scores) for i in scores]
            
            for i in range(gene_num):
                rnd = random.random()
                
                if rnd < mutation_rate:
                    # 突然変異
                    gene = genes[self.selection(genes, norm_scores)]
                    new_gene = self.mutation(gene)
                    new_genes.append(new_gene)
                elif rnd < mutation_rate + crossover_rate:
                    # 交叉
                    gene0 = genes[self.selection(genes, norm_scores)]
                    gene1 = genes[self.selection(genes, norm_scores)]
                    new_gene = self.crossover(gene0, gene1)
                    new_genes.append(new_gene)
                else:
                    # 選択
                    gene = genes[self.selection(genes, norm_scores)]
                    new_gene = copy.deepcopy(gene)
                    new_genes.append(new_gene)
            
            genes = new_genes
            new_genes = []
        
        best_automaton = self.gene_to_automaton(best_gene, "")
        print("Score: {}".format(best_score))
        print("States: {}".format(best_automaton.states))
        print("Transitions: {}".format(best_automaton.transitions))
        print(best_automaton.to_dfa_str())

def main():
    simulator = GeneticAlgorithmSimulator()
    simulator.run()

if __name__ == "__main__":
    main()
