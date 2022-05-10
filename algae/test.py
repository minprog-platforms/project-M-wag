   def __init__(self, width: int, height: int) -> None:
        """Create a new grid

        Args:
            width, height: the widt and height of the grid
        """
        default_val = 0.0
 
        self.height = height
        self.width = width
        #   Add Cache        
        self.grid =  []

        for x in range(self.width): 
            col = []
            for y in range(self.height):
                col.append(default_val)
            self.grid.append(col)
