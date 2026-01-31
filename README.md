# 🐾 ECO Autopet - 寵物過勞自動化系統

> 「拒絕寵物罷工，實現 24 小時全自動化血汗工廠！」 > 一個專為《ECO之夢》設計的 Python 輔助工具，讓你的寵物在你睡覺時也能勤奮加班。

![Python](https://www.google.com/search?q=https://img.shields.io/badge/Python-3.10%252B-blue) ![PySide6](https://www.google.com/search?q=https://img.shields.io/badge/GUI-PySide6-green) ![Platform](https://www.google.com/search?q=https://img.shields.io/badge/Platform-Windows-lightgrey)

## 📖 專案簡介 (Introduction)

你是否深受 ECO (Emil Chronicle Online) 寵物 AI 的困擾？只要主人發呆超過 10 分鐘，寵物就會開始偷懶、罷工，甚至直接無視怪物的攻擊？

ECO Autopet 是你的最佳解決方案！本程式透過 Win32 API 直接對遊戲視窗發送訊號，模擬玩家按鍵行為。最重要的是，它支援 後台運作 (Background Execution)，你可以在練寵的同時看影片、寫程式或玩其他遊戲，完全不影響滑鼠操作。

(｀・ω・´)ゞ 經測試確認：只要名字帶有 eco.exe 的視窗皆可穿透！

## ✨ 核心功能 (Features)

* ⚡ 後台穿透技術：使用 win32api.PostMessage，無需前台視窗焦點，不搶滑鼠，支援視窗最小化或被遮擋。
* * 🖥️ 多開同步支援：自動偵測所有 eco.exe 視窗，一次操作，全體寵物同步加班。
* * 🎮 自定義按鍵配置：     * F9 - F12：可獨立開關每個按鍵的觸發狀態。     * 推薦配置：F12 設為「坐下」，實現自動回魔 (MP Recovery) 循環。
* * ⏳ 靈活的時間控制：     * 自定義循環秒數（預設 180 秒）。     * 即時倒數顯示，掌握下一次「鞭策」寵物的時間。
* * 💻 輕量化浮窗設計：半透明置頂介面，隨時監控視窗數量與倒數狀態，點擊 X 即可一鍵下班。

## 🛠️ 安裝與執行 (Installation)

右邊release有exe檔，這個再不會真的沒辦法了...

## 🎮 使用說明 (Usage Guide)

開啟遊戲：啟動你的《ECO之夢》客戶端（支援多開）。

設定技能：在遊戲內將需要的技能或動作放入 F9 ~ F12 快捷鍵欄位。     * 建議：F12 放「坐下/站立」，F9~F11 放攻擊或Buff技能。

啟動本程式：執行腳本，會出現半透明浮窗。

參數設定：     * 輸入 循環時間 (秒)，點擊「設定」。     * 點擊上方的 F9/F10/F11/F12 按鈕來決定要觸發哪些按鍵（亮綠燈 = 開啟）。

開始掛機：程式會自動偵測所有遊戲視窗並開始倒數。即使你把遊戲視窗縮小，寵物依然會持續工作！

## ⚠️ 免責聲明 (Disclaimer)

* 本程式僅供技術研究與學術交流使用（Python Win32 API 學習）。 * 雖然GM表示此類程式合法，但使用任何自動化工具仍存在潛在風險，請低調使用。 * 請勿用於惡意破壞遊戲平衡或干擾其他玩家。 * 寵物過勞死本程式概不負責 (´・ω・`)。

--- Happy Farming! 祝您的寵物早日滿等！
