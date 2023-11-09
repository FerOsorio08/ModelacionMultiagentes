from mesa import Agent

class TreeCell(Agent):
    """
        A tree cell.
        
        Attributes:
            x, y: Grid coordinates
            condition: Can be "Dead", "On Fire", or "Burned Out"
            unique_id: (x,y) tuple.

            unique_id isn't strictly necessary here, but it's good practice to give one to each agent anyway.
    """

    def __init__(self, pos, model):
        """
        Create a new tree.

        Args:
            pos: The tree's coordinates on the grid.
            model: standard model reference for agent.
        """
        super().__init__(pos, model)
        self.pos = pos
        self.condition = "Dead"
        self._next_condition = None

    def step(self):
        """
        If the tree is on fire, spread it to Dead trees nearby.
        Revisa el alrededor 
        """

        if self.condition == "Dead":
            # for neighbor in self.model.grid.iter_neighbors(self.pos, True):
            #     if neighbor.condition == "Dead":
            #         neighbor._next_condition = "Alive"
            x, y = self.pos
            print("pos", self.pos)
        

            ##Conjunto de vivitos, condiciones para Alive
            vivitos = {"001","011","100","110"}
            ##String para guardar las condiciones de los vecinos
            aver = "000"

            for neighbor in self.model.grid.iter_neighbors(self.pos, True):
                x = (x +1 ) % 50
                y = (y +1) % 50
                ##Condiciones para Alive
                ## 1. Si el vecino diagonal izquierdo esta vivo
                if self.coordinates(neighbor) == (-1, -1) and neighbor.condition == "Alive":
                    print("entro a diagonal izquierda", self.coordinates(neighbor))
                    aver = aver[:0] + "1" + aver[1:]
                ## 2. Si el vecino de arriba esta vivo
                elif self.coordinates(neighbor) == (0, -1) and neighbor.condition == "Alive":
                    print("entro arriba", self.coordinates(neighbor))
                    aver = aver[:1] + "1" + aver[2:]
                ## 3. Si el vecino diagonal derecho esta vivo
                elif self.coordinates(neighbor) == (1, -1) and neighbor.condition == "Alive":
                    print("entro a diagonal derecha", self.coordinates(neighbor))
                    aver = aver[:2] + "1" + aver[3:]
            ##Checar si el arreglo actual esta en el conjunto de vivitos
            if aver in vivitos:
                self._next_condition = "Alive"
                    
            

    ##función para obtener las coordenadas de un agente
    def coordinates(self,other):
        
        return (self.pos[0] - other.pos[0], self.pos[1] - other.pos[1])
    
    def advance(self):
        """
        Advance the model by one step.
        previene el cambio de un solo agente
        """
        if self._next_condition is not None:
            self.condition = self._next_condition