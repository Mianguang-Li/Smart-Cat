# Android App

这是一个 Kivy Android 应用项目，使用 GitHub Actions 自动打包 APK。

## 项目结构

```
android_app/
├── main.py           # 应用主程序
├── buildozer.spec    # 打包配置
└── ...
```

## 如何使用

### 1. 推送代码到 GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/你的用户名/你的仓库名.git
git push -u origin main
```

### 2. 触发打包

- **自动触发**: 推送代码到 main/master 分支
- **手动触发**: 在 GitHub 仓库页面 → Actions → Build Android APK → Run workflow

### 3. 下载 APK

打包完成后：
1. 进入 Actions 页面
2. 点击完成的 workflow
3. 在 Artifacts 中下载 `android-apk`

## 本地测试

在推送前，可以在本地测试应用：

```bash
cd android_app
python main.py
```

## 自定义应用

- 修改 `main.py` 来改变应用功能
- 修改 `buildozer.spec` 来更改应用名称、图标、权限等

## 注意事项

- 首次打包可能需要 15-30 分钟
- 确保代码没有语法错误
- 如需添加依赖，在 `buildozer.spec` 的 `requirements` 中添加
