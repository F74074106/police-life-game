// 全域變數
let isQuiltFixed = false;
let isPillowFixed = false;
let isLadderFixed = false; 
let clutterCount = 4; // 記得確認你有 4 個雜物 (alarm, mask, power, phone)
let isCallMade = false;

// 更新狀態文字
function updateStatus(mainMsg, subMsg) {
    if (mainMsg) document.getElementById('message').innerText = mainMsg;
    if (subMsg) document.getElementById('sub-message').innerText = subMsg;
}

// 輔助函數：控制警告圖片顯示
function toggleFallImage(show) {
    const warningDiv = document.getElementById('image-warning');
    warningDiv.style.display = show ? 'block' : 'none';
}

// 1. 移除雜物
function removeItem(element) {
    element.style.transform = "scale(0)"; 
    setTimeout(() => { element.style.display = 'none'; }, 300);
    clutterCount--;
    checkProgress();
}

// 2. 整理棉被 (修正：配合 800px 的床寬)
function fixQuilt() {
    if (isQuiltFixed) return;

    const quilt = document.getElementById('quilt');
    
    // 配合 800px 寬度的設定
    quilt.style.width = '760px';     
    quilt.style.height = '340px';    
    quilt.style.top = '15px';        
    quilt.style.left = '30px';       
    quilt.style.bottom = 'auto';     
    quilt.style.transform = 'rotate(0deg)'; 
    
    // 🌟 關鍵修改：從顏色改為圖片 🌟
    // quilt.style.backgroundColor = '#388e3c'; <-- 刪除這行
    
    // 清除背景色，改用背景圖片
    quilt.style.backgroundColor = 'transparent'; 
    quilt.style.backgroundImage = "url('Quilt.png')";
    // 確保圖片填滿折好的區域
    quilt.style.backgroundSize = 'cover'; 
    
    // 如果你的 Quilt.png 圖片本身已經有直角了，可以把圓角設為 0
    quilt.style.borderRadius = '3px'; // 視圖片情況調整

    quilt.innerText = ""; 
    isQuiltFixed = true;
    // updateStatus(null, "棉被已折疊！");
    checkProgress();
}

// 3. 整理枕頭
function fixPillow() {
    if (isPillowFixed) return;

    const pillow = document.getElementById('pillow');
    
    // 🌟 修改：枕頭變立體
    pillow.style.transform = 'rotate(0deg)';
    pillow.style.width = '100px'; 
    pillow.style.height = '200px'; 
    
    // 定位在棉被左側上方
    pillow.style.top = '10px';      
    pillow.style.left = '690px';     
    
    // pillow.style.borderRadius = '5px'; 
    pillow.innerText = ""; 
    isPillowFixed = true;
    // updateStatus(null, "枕頭已定位！");
    checkProgress();
}

// 4. 移動螺絲修梯子
function moveScrewToLadder(clickedElement) {
    // 1. 如果梯子已經修好了，不用再點
    if (isLadderFixed) return;

    // 🌟 2. 新增檢查：如果還沒打過電話，不能拆螺絲
    if (!isCallMade) {
        // 可以選擇用 alert 彈窗，或是更新下方狀態列
        alert("公家財產不敢亂動...\n（是不是應該先打電話請示區隊長？）");
        updateStatus(null, "螺絲鎖得很緊，不敢隨便亂拆...");
        return; // 直接結束函數，不執行後面的動作
    }

    // --- 以下是原本的邏輯 (拆螺絲) ---
    const ladderScrew = document.getElementById('ladder-missing-screw');

    clickedElement.style.opacity = '0';
    clickedElement.style.cursor = 'default';
    clickedElement.onclick = null; 

    setTimeout(() => {
        ladderScrew.style.display = 'block';
        isLadderFixed = true;
        updateStatus(null, "梯子修好了！看起來很穩固。");
        checkProgress();
    }, 300);
}

// 5. 檢查進度
function checkProgress() {
    const isTidy = (clutterCount === 0 && isQuiltFixed && isPillowFixed);
    
    toggleFallImage(false);

    if (isTidy && !isLadderFixed) {
        updateStatus("內務整齊了");
        document.getElementById('message').style.color = "#d32f2f"; 
    } 
    else if (!isTidy && isLadderFixed) {
        updateStatus("內務混亂中", "床上還是很亂！趕快整理！");
        document.getElementById('message').style.color = "#d32f2f";
    }
    else if (isTidy && isLadderFixed) {
        updateStatus("準備完成！", " ");
        document.getElementById('message').style.color = "#2e7d32"; 
        document.getElementById('ladder').style.cursor = "pointer";
    }
}

// 6. 嘗試離開關卡
function tryExitLevel() {
    const isTidy = (clutterCount === 0 && isQuiltFixed && isPillowFixed);

    if (isTidy && isLadderFixed) {
        alert("恭喜過關！準備唱校歌！");
        // window.location.href = 'level2.html';
    } else {
        const ladder = document.getElementById('ladder');
        ladder.classList.add('shake-animation');
        
        setTimeout(() => {
            ladder.classList.remove('shake-animation');
        }, 500);

        if (isTidy && !isLadderFixed) {
            updateStatus("危險！", "差點摔死！或許可以打給劉區報修...?");
            toggleFallImage(true); 
        } 
        else if (!isLadderFixed) {
             updateStatus("內務混亂中", "內務還沒整理好，現在下去會被罵死！");
             document.getElementById('message').style.color = "#d32f2f";
        } else {
             updateStatus("內務混亂中", "內務還沒整理好，現在下去會被罵死！");
             document.getElementById('message').style.color = "#d32f2f";
        }
    }
}

// 7. 打開手機介面
function openPhone() {
    // 顯示遮罩層
    document.getElementById('phone-overlay').style.display = 'flex';
    
    // 重置手機畫面：確保每次打開都是回到主畫面
    document.getElementById('phone-view-home').style.display = 'block';
    document.getElementById('phone-view-call').style.display = 'none';
    
    // 重置輸入框和訊息
    document.getElementById('repair-code-input').value = '';
    document.getElementById('final-hint-message').style.display = 'none';
    document.getElementById('input-area').style.display = 'block';
}

// 8. 關閉手機介面
function closePhone() {
    document.getElementById('phone-overlay').style.display = 'none';
}

// 9. 顯示撥號畫面
function showCallScreen() {
    // 隱藏主畫面，顯示撥號畫面
    document.getElementById('phone-view-home').style.display = 'none';
    document.getElementById('phone-view-call').style.display = 'block';
}

// 10. 檢查輸入的代碼
function checkPhoneCode() {
    const inputField = document.getElementById('repair-code-input');
    const hintMessage = document.getElementById('final-hint-message');
    const inputArea = document.getElementById('input-area');

    const code = inputField.value;

    if (code === '4418') {
        // --- 答對了 ---
        
        // 🌟 新增：解鎖螺絲互動權限
        isCallMade = true;

        inputArea.style.display = 'none';
        
        hintMessage.innerText = "「時間來不及ㄌ 自己先找螺絲頂一下ㄅ」";
        hintMessage.style.display = 'block';
        
        // 提示玩家現在可以去拆螺絲了
        updateStatus(null, "獲得授權！快去拆標題旁的螺絲！");
        
    } else {
        alert("您撥的電話號碼是空號，請查明後再撥...");
        inputField.value = ''; 
    }
}