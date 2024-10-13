// ==UserScript==
// @name         宁畅日志辅助
// @namespace    http://tl.cooacloud.com/
// @version      2024-10-11
// @description  自动化日志操作辅助工具
// @author       Your Name
// @match        http://tl.cooacloud.com/worklog/
// @icon         https://www.google.com/s2/favicons?sz=64&domain=cooacloud.com
// @grant        none
// ==/UserScript==

(function () {
    'use strict';

    // 通用创建按钮函数
    function createStyledButton(text, top, right, backgroundColor) {
        const button = document.createElement('button');
        button.textContent = text;
        Object.assign(button.style, {
            position: 'fixed',
            top: top,
            right: right,
            zIndex: '9999',
            backgroundColor: backgroundColor,
            color: 'white',
            border: 'none',
            padding: '10px 20px',
            fontSize: '16px',
            fontWeight: 'bold',
            borderRadius: '5px',
            cursor: 'pointer',
            boxShadow: '0 2px 5px rgba(0,0,0,0.2)',
            marginBottom: '10px' // 添加底部间距
        });

        button.onmouseover = () => button.style.backgroundColor = shadeColor(backgroundColor, -10);
        button.onmouseout = () => button.style.backgroundColor = backgroundColor;

        document.body.appendChild(button);
        return button;
    }

    // 颜色调整函数
    function shadeColor(color, percent) {
        const f = parseInt(color.slice(1), 16), t = percent < 0 ? 0 : 255, p = percent < 0 ? percent * -1 : percent,
            R = f >> 16, G = f >> 8 & 0x00FF, B = f & 0x0000FF;
        return "#" + (0x1000000 + (Math.round((t - R) * p) + R) * 0x10000 + (Math.round((t - G) * p) + G) * 0x100 + (Math.round((t - B) * p) + B)).toString(16).slice(1);
    }

    // 创建按钮
    const autoSelectButtonNext = createStyledButton('选择日期', '350px', '100px', '#2196F3');
    const autoSelectButton = createStyledButton('点击自动选择', '60px', '10px', '#4CAF50');
    const setNoonTimeButton = createStyledButton('上午', '110px', '10px', '#FF9800');
    const setAfternoonTimeButton = createStyledButton('下午', '160px', '10px', '#9C27B0');
    const setEveningTimeButton = createStyledButton('晚上', '210px', '10px', '#E91E63');

    // 点击元素函数
    function clickElement(selector) {
        const element = document.querySelector(selector);
        if (element) {
            element.click();
            console.log(`点击了 "${selector}"`);
        } else {
            console.log(`没有找到 "${selector}"`);
        }
    }

    // 延迟执行函数
    function delayExecution(func, delay) {
        return new Promise(resolve => setTimeout(() => {
            func();
            resolve();
        }, delay));
    }

    // 设置输入框值并触发change事件
    function setInputValueAndTriggerChange(selector, value) {
        const input = document.querySelector(selector);
        if (input) {
            input.value = value;
            const event = new Event('change', { bubbles: true });
            input.dispatchEvent(event);
            console.log(`设置 ${selector} 的值为 ${value}`);
        } else {
            console.log(`没有找到 ${selector}`);
        }
    }

    // 选择日期按钮点击事件
    autoSelectButtonNext.addEventListener('click', async function () {
        await delayExecution(() => clickElement('button.btn.btn-primary.btn-sm.btn-outline[onclick="worklog_add_event()"]'), 1000);
        await delayExecution(() => clickElement('label.btn.btn-sm.btn-primary[onclick="create_worklog();"]'), 500);
    });

    // 自动选择按钮点击事件
    autoSelectButton.addEventListener('click', async function () {
        clickElement('div.project_item[data-project_id="64cdac207bda66be6c78bb1c"]');
        clickElement('div.characteristic_item[data-id="5f3d209182ca8553dc54794c"]');

        const buttons = document.querySelectorAll('div.flex.flex-row.items-center.w-full');
        if (buttons.length > 5) buttons[5].click();

        await delayExecution(() => clickElement('label.btn.btn-sm.btn-primary[onclick="confirm_project_setting()"]'), 500);
    });

    // 设置上午时间按钮点击事件
    setNoonTimeButton.addEventListener('click', function () {
        setInputValueAndTriggerChange('input.flex-1.w-full.time.start.ui-timepicker-input.input.input-bordered.input-xs', '09:00');
        setInputValueAndTriggerChange('input.flex-1.w-full.time.end.ui-timepicker-input.input.input-bordered.input-xs', '12:00');
    });

    // 设置下午时间按钮点击事件
    setAfternoonTimeButton.addEventListener('click', function () {
        setInputValueAndTriggerChange('input.flex-1.w-full.time.start.ui-timepicker-input.input.input-bordered.input-xs', '13:00');
        setInputValueAndTriggerChange('input.flex-1.w-full.time.end.ui-timepicker-input.input.input-bordered.input-xs', '18:00');
    });

    // 设置晚上时间按钮点击事件
    setEveningTimeButton.addEventListener('click', function () {
        setInputValueAndTriggerChange('input.flex-1.w-full.time.start.ui-timepicker-input.input.input-bordered.input-xs', '19:00');
        setInputValueAndTriggerChange('input.flex-1.w-full.time.end.ui-timepicker-input.input.input-bordered.input-xs', '21:00');
    });
})();