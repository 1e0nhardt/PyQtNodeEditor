# PyQtNodeEditor
一个用PyQt实现的节点编辑器

[Pavel Křupala的Youtube视频教程](https://www.youtube.com/watch?v=xbTLhMJARrk&list=PLZSNHzwDCOggHLThIbCxUhWTgrKVemZkz)

## Note
## 贝塞尔曲线的选择范围
存在起点和终点相同的直线和贝塞尔曲线时，选择不到直线。

## cookiecutter
1. 安装: `pip install cookiecutter`
2. 创建模板: `cookiecutter gh:audreyfeldroy/cookiecutter-pypackage`，填入各种信息
3. 模仿模板创建项目结构
4. 创建项目包
    - 测试安装: `pip install -e .`
    - 源码包: `python setup.py sdist`
    - wheel: `python setup.py bdist_wheel`
    - wheel的安装: `pip install wheel_file.whl`
5. 测试: tox
6. MANIFEST.in 声明那些文件会为包含在package中
7. 创建文档: sphinx, sphinx_rtd_theme
8. 从github安装: `pip install git+https://github.com/1e0nhardt/PyQtNodeEditor.git`

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
- 用Scene类管理QDMGraphicsScene，QDMGraphicsScene也保存Scene的引用
- Scene类保存场景中的内容
- QDMGraphicsScene负责背景绘制

### ep5
- Node类保存节点数据
- QDMGraphicsNode负责外观和交互
    - 重写QGraphicsItem的paint方法设置外观
- QPainterPath
    - addRoundedRect 绘制圆角矩形
    - addRect 绘制矩形
    - 上半圆角，下半直角的矩形：圆角矩形+两个矩形盖住两个角

### ep6
- QGraphicsProxyWidget
    - QGraphicsProxyWidget 是 PyQt 中的一个类，用于将 QWidget 或其子类包装为 QGraphicsItem，以便在图形场景中进行显示和交互。  
    - QGraphicsProxyWidget 充当 QWidget 和 QGraphicsItem 之间的桥梁，使得可以在图形场景中使用 QWidget 的功能，并可以通过 QGraphicsItem 的属性和方法对其进行控制。
- 设置全局样式: QApplication.instance().setStyleSheet(str(styleSheet, encoding='utf-8'))

### ep7
- Socket
- QDMGraphicsSocket
- 计算位置画点

### ep8
- Edge
- QDMGraphicsEdge继承QGraphicsPathItem
    - QGraphicsPathItem有一个path()方法返回定义的 path。paint方法中只要把这个path画出来即可。
    - 直线 path.lineTo(x, y)
    - Bezier曲线 path.cubicTo(c1x, c1y, c2x, c2y, x, y)

### ep9
- Edge和Socket交互，获取起点和终点位置

### ep10
- 在QDMGraphicsNode的mouseMoveEvent中更新关联的Edge的位置
- 将socket颜色和类型挂钩

### ep11
- 确定连接Edge的逻辑
- 左键点击和拖动ES
- 左键点击和释放 
- 左键点击和释放到ES 
- ctrl+左键拖动边到已存在的ES时，替换

### ep12
- 使用rich打印日志和错误信息
- 完成连接边的逻辑
    - 问题：如果一个socket有边，以其为起点连接新边后，原来的边和socket解绑了，因此会边的端点会固定在连接位置
    - 解决方法：删除之前的边
    - 目前一个socket只能连一条边
- 优化了贝塞尔曲线

### ep13
- FixBug: 
    - 松开中键时，dragMode由NoDrag换为默认的RubberBandDrag。(x)
    - 在场景中按下左键时，将dragMode设为RubberBandDrag，松开时设回NoDrag
    - 伪造QMouseEvent时, 第三个参数为全局位置，用globalPosition()而不是scenePosition().
        - scenePosition()和position()返回值一样
        - 要获取在scene中的位置还是需要用mapToScene
- 添加qss，使框选区域背景色为白色
- 将Ctrl+左键的多选功能绑定到Shift+左键
- 节点移动时更新当前节点相关边，更改为更新所有选中节点的相关边

### ep20
- 问题：序列化时，可序列化目标的id使用的是id(self)，即内存地址。反序列化时，会清除scene中的所有对象并按记录重新创建。这样，反序列化后，同样的场景，id全变了，因此不能通过文件中记录的id索引到相应对象了。
- 原作者通过重新将反序列化后的对象的self.id重新设置为记录中的id解决了该问题。
- 这里id虽然存的是内存地址，但可以只将其当做一个进程唯一的标识符。

### ep21
- 菜单选项名称中的'&'的作用是助记符，按下alt键后，标记的字符下会出现下划线。再按下字符对应的按键，即可快捷触发相应选项。