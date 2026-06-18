# Hermes Doomsday Backup

## 末日恢复
```bash
curl -sL https://raw.githubusercontent.com/zcs366/izu/backup/doomsday-recover.sh -o /tmp/doomsday-recover.sh && bash /tmp/doomsday-recover.sh
```

## 说明
- `backup-*.tar.gz` — Hermes 公开数据备份（不含密钥，不含会话历史）
- 全量备份(2.1G)保存在本机 `/mnt/i/hermes/output/备份/`
- `.env` 密钥文件需从本机 `output/备份/` 手工恢复

Backup timestamp: 20260618_200355
Doomsday archive: 68M compressed
