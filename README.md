# Python STUN 服务端

## 使用方法

1. 克隆或下载 `stun.py` 文件到本地。
2. 在终端运行以下命令启动 STUN 服务端：

   ```bash
   python stun.py
   ```

3. STUN 服务端会开始监听并等待客户端请求。

## 配置

- 默认端口：`5000`
- 默认协议：`UDP` 和 `TCP`

> 注意：确保防火墙允许所需端口的通信。

## 依赖

- Python 版本：`3.x`
- 相关库：`socket`, `asyncio`

## 更多

- 自定义端口和配置请参考 `stun.py` 中的参数设置。
- 欢迎提 PR 或在 Issues 中报告 Bug！
