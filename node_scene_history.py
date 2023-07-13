from utils import logger

class SceneHistory():

    def __init__(self, scene):
        self.scene = scene

        self.history_stack = []
        self.history_current_step = -1
        self.history_limit = 8

    def undo(self):
        logger.debug("[pink3]UNDO[/]")

        if self.history_current_step > 0:
            self.history_current_step -= 1
            self.restoreHistory()

    def redo(self):
        logger.debug("[pink3]REDO[/]")

        if self.history_current_step + 1 < len(self.history_stack):
            self.history_current_step += 1
            self.restoreHistory()

    def restoreHistory(self):
        logger.debug(f"[pink3]Restoring history[/] .... current_step: #{self.history_current_step} ({len(self.history_stack)})")
        self.restoreHistoryStamp(self.history_stack[self.history_current_step])

    def storeHistory(self, desc):
        # history_current_step没有指向栈头时去除之后的记录。(undo过)
        if self.history_current_step+1 < len(self.history_stack):
            self.history_stack = self.history_stack[0:self.history_current_step+1]

        # 超出历史记录上限时，删除栈尾的记录。
        if self.history_current_step+1 >= self.history_limit:
            self.history_stack = self.history_stack[1:]
            self.history_current_step -= 1
        
        hs = self.createHistoryStamp(desc)
        self.history_stack.append(hs)
        self.history_current_step += 1

        logger.debug(f"[pink3]Storing history[/] {desc} current_step: #{self.history_current_step} ({len(self.history_stack)})")

    def createHistoryStamp(self, desc):
        return desc

    def restoreHistoryStamp(self, history_stamp):
        logger.debug(f"RHS: {history_stamp}")
