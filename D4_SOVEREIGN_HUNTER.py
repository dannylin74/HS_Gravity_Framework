"""
[戰術代號: D4_SOVEREIGN_HUNTER.py]
[主權版本: V3.7 - High Entropy Combat Mode]
[功能: 運用數理引力場與幾何雜湊，實現《暗黑破壞神 4》的自主導航與戰鬥]
"""

import time
from SOVEREIGN_VISION_STACK import vision_stack
from SOVEREIGN_INPUT_GATEWAY import stealth_input
from SOVEREIGN_SEMANTIC_DEDUCTOR import deductor

class D4SovereignAgent:
    def __init__(self):
        self.mode = "HUNTING"
        # 預設戰術權重 (由 Sage 動態調整)
        self.weights = {
            "COMBAT": 0.8,
            "LOOT": 0.4,
            "SURVIVAL": 1.0
        }
        print("⚔️ [D4_Hunter] 主權獵人已點火。等待指揮官戰術授權。")

    def set_tactical_weights(self, strategy_json):
        """接收來自 Sage 的戰術參數"""
        new_weights = json.loads(strategy_json)
        self.weights.update(new_weights)
        print(f"📡 [D4_Hunter] 戰術權重已更新: {self.weights}")

    def run_combat_loop(self):
        """
        [主權戰鬥循環]: 感知 -> 坍縮 -> 執行
        """
        while True:
            # 1. 掃描戰場 (高熵感知)
            # 鎖定血量球 (HP) 與 目標怪堆 (ENEMIES)
            hp_pos, _ = vision_stack.find_element("HEALTH_GLOBE")
            enemy_pos, _ = vision_stack.find_element("ENEMY_CLUSTER")

            # 2. 數理演繹與引力計算
            # 根據血量狀態與敵人距離決定行動
            intent = deductor.deduce_action(enemy_pos, "DIABLO_UNIT", "#FF0000", 0.95)

            if intent == "FORCE_STOP": # 緊急低血量
                self._emergency_retreat()
                continue

            if intent == "PROCEED_WITH_PHYSICAL_GRAVITY":
                # 執行「引力點火」: 向怪堆移動並施放技能
                x, y = enemy_pos
                stealth_input.move_mouse_stealth(x, y)
                stealth_input.click_stealth(button='right') # 核心技能
                
            time.sleep(0.1) # 10Hz 戰鬥頻率

    def _emergency_retreat(self):
        """緊急撤退邏輯"""
        print("⚠️ [D4_Hunter] 生命體徵危急，執行緊急位移！")
        # 向螢幕中心反方向移動
        stealth_input.click_stealth(1280, 720, button='space') # 閃避

# 初始化獵人
d4_hunter = D4SovereignAgent()
