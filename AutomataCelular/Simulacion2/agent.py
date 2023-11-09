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
        x, y = self.pos
        # x = x % 50  # Apply % 50 to x
        # y = y % 50  # Apply % 50 to y

        #Conjunto de vivitos, condiciones para Alive
        vivitos = {"001", "011", "100", "110"}
        #String para guardar las condiciones de los vecinos
        aver = "000"
        
        for neighbor in self.model.grid.iter_neighbors(self.pos, True):
            #X y Y son las coordenadas del vecino se hacen % 50 para que no se salgan del grid
            x = (x ) % 50  # Apply % 50 to x
            y = (y ) % 50  # Apply % 50 to y
            # if aver in vivitos:
            #     self._next_condition = "Alive"
            # # x = (x + 1) % 50
            # # y = (y + 1) % 50
            # else:
            #     self._next_condition = "Dead"

            if self.coordinates(neighbor) == (-1, -1) and neighbor.condition == "Alive":
                print("entro a diagonal izquierda", self.coordinates(neighbor))
                aver = aver[:0] + "1" + aver[1:]
                # x = (x + 1) % 50  # Apply % 50 to x
                # y = (y + 1) % 50  # Apply % 50 to y
            elif self.coordinates(neighbor) == (0, -1) and neighbor.condition == "Alive":
                print("entro arriba", self.coordinates(neighbor))
                aver = aver[:1] + "1" + aver[2:]
                # x = (x + 1) % 50  # Apply % 50 to x
                # y = (y + 1) % 50  # Apply % 50 to y
            elif self.coordinates(neighbor) == (1, -1) and neighbor.condition == "Alive":
                print("entro a diagonal derecha", self.coordinates(neighbor))
                aver = aver[:2] + "1" + aver[3:]
            
            
        #Checar si el arreglo actual esta en el conjunto de vivitoss
        if aver in vivitos:
            self._next_condition = "Alive"
            # x = (x + 1) % 50
            # y = (y + 1) % 50
        else:
            self._next_condition = "Dead"
            x = (x - 1) % 50
            y = (y - 1) % 50

        # Update the position after applying % 50
        self.pos = (x, y)
            
            
            

    #Función para obtener las diferencias de coordenadas de un agente
    def coordinates(self,other):
        return ((self.pos[0]) - (other.pos[0]),(self.pos[1]) - (other.pos[1]))
    
    def advance(self):
        """
        Advance the model by one step.
        previene el cambio de un solo agente
        """
        if self._next_condition is not None:
            self.condition = self._next_condition