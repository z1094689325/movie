'''参考：https://www.cnblogs.com/wangyongsong/p/6750454.html'''一、特性（property）import mathclass Circle:    def __init__(self,radius): #圆的半径radius        self.radius=radius    @property    def area(self):        return math.pi * self.radius**2 #计算面积    @property    def perimeter(self):        return 2*math.pi*self.radius #计算周长c=Circle(10)print(c.radius)print(c.area) #可以向访问数据属性一样去访问area,会触发一个函数的执行,动态计算出一个值print(c.perimeter) #同上'''输出结果:314.159265358979362.83185307179586注意：此时的特性arear和perimeter不能被赋值'''