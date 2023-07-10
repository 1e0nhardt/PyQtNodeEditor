# PyQtNodeEditor
一个用PyQt实现的节点编辑器

[Pavel Křupala的Youtube视频教程](https://www.youtube.com/watch?v=xbTLhMJARrk&list=PLZSNHzwDCOggHLThIbCxUhWTgrKVemZkz)

## QGraphicsProxyWidget
QGraphicsProxyWidget 是 PyQt 中的一个类，用于将 QWidget 或其子类包装为 QGraphicsItem，以便在图形场景中进行显示和交互。  
QGraphicsProxyWidget 充当 QWidget 和 QGraphicsItem 之间的桥梁，使得可以在图形场景中使用 QWidget 的功能，并可以通过 QGraphicsItem 的属性和方法对其进行控制。

## 贝塞尔曲线的选择范围
存在起点和终点相同的直线和贝塞尔曲线时，选择不到直线。

## ep11
ES: End Socket

- 左键点击和拖动ES
- 左键点击和释放 
- 左键点击和释放到ES 
- ctrl+左键拖动边到已存在的ES时，替换