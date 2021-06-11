
[掘金介绍](https://juejin.cn/post/6972339726657421342/)

## 需要配置的信息

### 钉钉机器人
可以参考[钉钉文档](https://ding-doc.dingtalk.com/doc#/serverapi2/qf2nxq)。

```python
ding_Talk_rboot = '' 
ding_Talk_secret=''
```

### 蒲公英

```python
pgy_uKey = ""
pgy_api_key = ""
```

### 人员配置

```python
# 手机号
one_phone = '16666666666' # 
two_phone ='16666666666' # 
three_phone = '16666666666' # 
four_phone ='16666666666' # 
five_phone ='16666666666' # 
```


> 提醒：本文不介绍 Xcode Server 的基本配置过程

Xcode Server 是 Apple 公司提供的持续集成方案，在 Xcode 9 之前需要在 Mac App Store 下载并安装 OS X Server。在Xcode 9中，Xcode Server被内置在了Xcode中，整个 CI 环境搭建过程大大的简化了。

Xcode Server 构建结束之后，可以看到构建过程中产生的各种数据，比如，在的 Commits 界面中，展示了本次集成和上次相比新增的 Git 提交记录。

![image.png](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/8a250153b0db44d8bd66d25cdcf3a033~tplv-k3u1fbpfcp-zoom-1.image)

通常会将 Xcode Server 部署到一台单独的 Mac 上，当需要打包的时候，把代码合并到指定的分支上，Xcode Server 就会自动打包。

构建结束之后，如何将构建信息通知到开发人员、测试人员以及项目负责人呢？让所有的人员都盯着 Xcode Server 上的信息么？显然在公司的沟通工具（钉钉）中推送一条信息，并 @ 相关的人，是最方便的了。

下面是最终的实现展示，输出了尽可能详细的构建信息：编译信息、上传蒲公英的信息、代码变更记录、@ 相关的人员。

![WechatIMG124的副本.jpeg](https://p9-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/7619b089b0ea441cb3130371070cb4a5~tplv-k3u1fbpfcp-watermark.image)

提醒：使用 Xcode Server 提供了直接下载、安装 App 的功能，但是需要通过 HTTPS 进行访问，所以需要保证手机和 Xcode Server 在一个网段内，或者部署到 HTTPS 环境下。如果不能保证再考虑将 ipa 上传到蒲公英等相关分发平台。

下面介绍如何提取钉钉消息中的相关信息。

# 如何提取编译信息

Xcode Server 提供了很多[环境变量](https://andrewmika.gitbooks.io/xcode-server-and-continuous-integration-guide-cn/content/5.html)，构建结束之后直接使用即可。

# 如何提取版本信息

在通过 [API](https://www.pgyer.com/doc/view/api#uploadApp) 将 ipa 提交到[蒲公英](https://www.pgyer.com/)后，会返回这部分的信息。

# 如何代码提交记录

首先要注意一点，Xcode Server 会从 Git 仓库拉取一份代码，放到自己专门项目路径，和我们拉取的项目路径并不是同一个。

环境变量 `XCS_PRIMARY_REPO_DIR` 提供了 Xcode Server 的工作空间的源代码存储库的路径。我们可以使用 python 库 `Repo` 来获取 Git 的 commit 信息。

但是如何获取本次构建相对于上次新增的 commit 信息呢？也就是如何获取上次构建的时候最后一次 commit 的信息呢？

环境变量 `XCS_OUTPUT_DIR` 提供了 Xcode Server 集成期间存储的资源（包括日志和产品）的顶级目录。
'XCS_OUTPUT_DIR' + "/sourceControl.log" 就是本地构建的日志信息。

```
// 一段日志信息
DVTSourceControlWorkspaceBlueprintLocationsKey =     {
    B18B82A392A550FBEAB693A1A84AE2228193F564 =         {
        DVTSourceControlBranchIdentifierKey = master;
        DVTSourceControlBranchOptionsKey = 4;
        DVTSourceControlBranchRemoteNameKey = origin;
        DVTSourceControlLocationRevisionKey = f7c3ccf7d8678fb26ae3700e747e057bd0b17c0f;
        DVTSourceControlWorkspaceBlueprintLocationTypeKey = DVTSourceControlBranch;
    };
};
```

其中 `DVTSourceControlLocationRevisionKey` 节点包含了上次构建时的 commit 信息。

至此，Git 的 commit 信息就可以获取到了，总结一下：
1. 环境变量 `XCS_PRIMARY_REPO_DIR` 为 Xcode Server 的源码路径；
1. python 库 `Repo` 可以用来提起 commit 信息；
1. `sourceControl.log` 中 `DVTSourceControlLocationRevisionKey` 包含了上次构建的 commit 信息。


本文的[项目地址](https://github.com/FuYouFang/XcodeServerConfig)，可以查看所有相关代码。

