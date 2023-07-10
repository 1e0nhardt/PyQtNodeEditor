# PyQtNodeEditor
一个用PyQt实现的节点编辑器

[Pavel Křupala的Youtube视频教程](https://www.youtube.com/watch?v=xbTLhMJARrk&list=PLZSNHzwDCOggHLThIbCxUhWTgrKVemZkz)

## Note
## QGraphicsProxyWidget
QGraphicsProxyWidget 是 PyQt 中的一个类，用于将 QWidget 或其子类包装为 QGraphicsItem，以便在图形场景中进行显示和交互。  
QGraphicsProxyWidget 充当 QWidget 和 QGraphicsItem 之间的桥梁，使得可以在图形场景中使用 QWidget 的功能，并可以通过 QGraphicsItem 的属性和方法对其进行控制。

## 贝塞尔曲线的选择范围
存在起点和终点相同的直线和贝塞尔曲线时，选择不到直线。

## Summary
### ep1
- 节点编辑器用QGraphicsView组件实现。
    - QGraphicsView组件包含一个QGraphicsScene可以实现画布功能
    - QGraphicsScene可以添加QGraphicsItem
    - 通过重写QGraphicsScene的drawBackground方法实现网格背景
- 用 QVBoxLayout 设置无边框，并让QGraphicsView组件大小跟随窗口

### ep2
- QGraphicsScene可以添加各种QGraphicsItem
    - scene.addText
    - scene.addRect
    - scene.addLine
    - scene.addWidget
- 各种QGraphicsItem通过setFlag可以实现各种功能
    - QGraphicsItem.GraphicsItemFlag.ItemIsMovable
    - QGraphicsItem.GraphicsItemFlag.ItemIsSelectable
- QGraphicsView
    - 通过setRenderHints设置渲染质量
    - 通过setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)强制完整重绘防止残影等问题
    - 通过setHorizontalScrollBarPolicy等去除滚动条

### ep3
- 用QGraphicsView提供的功能实现画布的缩放以及拖动
    - 缩放: scale(zoom_factor, zoom_factor)
        - 设置缩放锚点为鼠标位置 setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
    - 拖动
        - 利用QGraphicsView提供的功能setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        - setDragMode(QGraphicsView.DragMode.ScrollHandDrag)需要按住鼠标左键才能拖动
        - 通过构造一个左键释放事件保证左键在进入DragMode模式前空闲
        - 进入DragMode模式后再构造一个左键按下事件
        - 松开中键，self.setDragMode(QGraphicsView.DragMode.NoDrag)前，再构造一个左键释放事件
        - 于是实现了中键拖动

### ep4


### ep11
ES: End Socket

- 左键点击和拖动ES
- 左键点击和释放 
- 左键点击和释放到ES 
- ctrl+左键拖动边到已存在的ES时，替换