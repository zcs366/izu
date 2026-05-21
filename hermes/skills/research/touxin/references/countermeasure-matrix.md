# 透心对策矩阵

见 data/touxin-countermeasure-matrix.json。

5种已知反爬模式：
- captcha_triggered — 触发验证码
- content_too_short — 内容被截断/空壳
- network_timeout — 网络超时
- login_required — 需要登录
- zse_ck_upgraded — zse_ck加密升级

自适应引擎工作流：
1. 抓取失败 → diagnose_failure()诊断模式
2. get_countermeasures()获取对策（按成功率降序）
3. 逐个try_countermeasure()
4. update_success_rate()更新成功率（指数移动平均，α=0.3）
5. 全部失败→记录新模式→通知用户
