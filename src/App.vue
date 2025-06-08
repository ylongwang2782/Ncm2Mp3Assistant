<template>
  <div class="container">
    <el-tabs v-model="activeTab">
      <el-tab-pane label="拖放转换" name="single">
        <div class="conversion-form">
          <div 
            class="drop-area"
            @dragover.prevent="handleDragOver"
            @dragleave.prevent="handleDragLeave"
            @drop.prevent="handleFileDrop"
            :class="{ 'is-dragover': isDragover }"
          >
            <el-icon class="drop-icon"><Upload /></el-icon>
            <div class="drop-text">
              将 NCM 文件拖放到此处，或
              <el-button type="primary" link @click="selectSingleFile">点击选择文件</el-button>
            </div>
            <div class="drop-hint">支持单个或多个 NCM 文件</div>
          </div>

          <div v-if="pendingFiles.length > 0" class="file-list">
            <div class="list-header">
              <h4>待转换文件 ({{ pendingFiles.length }})</h4>
              <el-button type="danger" size="small" @click="clearPendingFiles">清空列表</el-button>
            </div>
            <el-table :data="pendingFiles" style="width: 100%" height="300">
              <el-table-column prop="name" label="文件名" min-width="200">
                <template #default="scope">
                  <el-tooltip :content="scope.row.path" placement="top">
                    <span>{{ scope.row.name }}</span>
                  </el-tooltip>
                </template>
              </el-table-column>
              <el-table-column prop="size" label="大小" width="120">
                <template #default="scope">
                  {{ formatFileSize(scope.row.size) }}
                </template>
              </el-table-column>
              <el-table-column label="操作" width="120">
                <template #default="scope">
                  <el-button 
                    type="danger" 
                    link 
                    @click="removeFile(scope.$index)"
                  >
                    移除
                  </el-button>
                </template>
              </el-table-column>
            </el-table>

            <div class="conversion-options">
              <div class="option-row">
                <el-checkbox v-model="useCustomOutput">自定义输出位置</el-checkbox>
                <el-input v-model="singleOutput" readonly v-if="useCustomOutput">
                  <template #append>
                    <el-button @click="selectSingleOutput">浏览</el-button>
                  </template>
                </el-input>
              </div>
              <div class="option-row">
                <el-checkbox v-model="deleteOriginal">转换完成后删除原文件</el-checkbox>
              </div>
            </div>

            <div class="action-buttons">
              <el-button 
                type="primary" 
                @click="convertFiles" 
                :loading="converting"
                :disabled="pendingFiles.length === 0"
              >
                开始转换
              </el-button>
            </div>
          </div>
        </div>
      </el-tab-pane>

      <el-tab-pane label="文件夹转换" name="batch">
        <div class="conversion-form">
          <el-form label-position="top">
            <el-form-item label="输入文件夹">
              <el-input v-model="batchInput" readonly>
                <template #prepend>
                  <el-icon><Folder /></el-icon>
                </template>
                <template #append>
                  <el-button @click="selectBatchInput">浏览</el-button>
                </template>
              </el-input>
            </el-form-item>
            
            <el-form-item label="输出文件夹">
              <el-checkbox v-model="useCustomBatchOutput">自定义输出位置</el-checkbox>
              <el-input v-model="batchOutput" readonly v-if="useCustomBatchOutput">
                <template #prepend>
                  <el-icon><Folder /></el-icon>
                </template>
                <template #append>
                  <el-button @click="selectBatchOutput">浏览</el-button>
                </template>
              </el-input>
            </el-form-item>

            <el-form-item>
              <el-checkbox v-model="deleteBatchOriginal">转换完成后删除原文件</el-checkbox>
            </el-form-item>

            <el-form-item>
              <el-button 
                type="primary" 
                @click="convertBatch" 
                :loading="converting"
                :disabled="!batchInput"
              >
                开始转换
              </el-button>
            </el-form-item>
          </el-form>
        </div>
      </el-tab-pane>

      <el-tab-pane label="转换记录" name="history">
        <div class="history-container">
          <div class="history-header">
            <h3>转换记录</h3>
            <el-button type="danger" size="small" @click="clearHistory" :disabled="!conversionHistory.length">
              清空记录
            </el-button>
          </div>
          <el-table :data="conversionHistory" style="width: 100%" height="400">
            <el-table-column prop="timestamp" label="转换时间" width="180">
              <template #default="scope">
                {{ formatDate(scope.row.timestamp) }}
              </template>
            </el-table-column>
            <el-table-column prop="inputFile" label="输入文件" min-width="200">
              <template #default="scope">
                <el-tooltip :content="scope.row.inputFile" placement="top">
                  <span>{{ getFileName(scope.row.inputFile) }}</span>
                </el-tooltip>
              </template>
            </el-table-column>
            <el-table-column prop="outputFile" label="输出文件" min-width="200">
              <template #default="scope">
                <el-tooltip :content="scope.row.outputFile" placement="top">
                  <span>{{ getFileName(scope.row.outputFile) }}</span>
                </el-tooltip>
              </template>
            </el-table-column>
            <el-table-column prop="status" label="状态" width="100">
              <template #default="scope">
                <el-tag :type="scope.row.status === 'success' ? 'success' : 'danger'">
                  {{ scope.row.status === 'success' ? '成功' : '失败' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="error" label="错误信息" min-width="200" v-if="hasErrors">
              <template #default="scope">
                <span v-if="scope.row.error" class="error-message">{{ scope.row.error }}</span>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-tab-pane>

      <el-tab-pane label="关于" name="about">
        <div class="about-container">
          <h2>NCM to MP3 Assistant</h2>
          <div class="version">版本：{{ version }}</div>
          
          <div class="section">
            <h3>功能特点</h3>
            <ul>
              <li>支持单个或多个 NCM 文件拖放转换</li>
              <li>支持整个文件夹批量转换</li>
              <li>可选择是否保留原文件</li>
              <li>支持自定义输出位置</li>
              <li>实时显示转换进度</li>
              <li>保存转换历史记录</li>
            </ul>
          </div>

          <div class="section">
            <h3>使用说明</h3>
            <h4>拖放转换</h4>
            <ol>
              <li>将 NCM 文件拖入虚线框内，或点击选择文件</li>
              <li>可以添加多个文件到转换列表</li>
              <li>选择是否自定义输出位置</li>
              <li>选择是否删除原文件</li>
              <li>点击"开始转换"按钮</li>
            </ol>

            <h4>文件夹转换</h4>
            <ol>
              <li>选择包含 NCM 文件的输入文件夹</li>
              <li>选择是否自定义输出位置</li>
              <li>选择是否删除原文件</li>
              <li>点击"开始转换"按钮</li>
            </ol>
          </div>

          <div class="section">
            <h3>项目信息</h3>
            <p>GitHub 仓库：<a href="https://github.com/ylongwang2782/Ncm2Mp3Assistant" target="_blank">https://github.com/ylongwang2782/Ncm2Mp3Assistant</a></p>
          </div>
        </div>
      </el-tab-pane>
    </el-tabs>

    <el-dialog v-model="progressVisible" title="转换进度" width="30%">
      <el-progress :percentage="progress" :status="progressStatus"></el-progress>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="progressVisible = false">关闭</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
const { ipcRenderer } = require('electron');
const { PythonShell } = require('python-shell');
const fs = require('fs');
const path = require('path');
import { Upload, Folder } from '@element-plus/icons-vue'
import packageJson from '../package.json'

export default {
  name: 'App',
  components: {
    Upload,
    Folder
  },
  data() {
    return {
      version: packageJson.version,
      activeTab: 'single',
      singleInput: '',
      singleOutput: '',
      batchInput: '',
      batchOutput: '',
      useCustomOutput: false,
      useCustomBatchOutput: false,
      converting: false,
      progressVisible: false,
      progress: 0,
      progressStatus: '',
      conversionHistory: [],
      isDragover: false,
      pendingFiles: [],
      deleteOriginal: false,
      deleteBatchOriginal: false
    }
  },
  computed: {
    hasErrors() {
      return this.conversionHistory.some(record => record.error);
    }
  },
  methods: {
    formatFileSize(bytes) {
      if (bytes === 0) return '0 B';
      const k = 1024;
      const sizes = ['B', 'KB', 'MB', 'GB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    },
    handleDragOver(e) {
      this.isDragover = true;
    },
    handleDragLeave(e) {
      this.isDragover = false;
    },
    handleFileDrop(e) {
      this.isDragover = false;
      const files = Array.from(e.dataTransfer.files);
      const ncmFiles = files.filter(file => file.path.toLowerCase().endsWith('.ncm'));
      
      if (ncmFiles.length === 0) {
        this.$message.error('请选择 NCM 格式的文件');
        return;
      }

      const newFiles = ncmFiles.map(file => ({
        name: file.name,
        path: file.path,
        size: file.size
      }));

      this.pendingFiles = [...this.pendingFiles, ...newFiles];
    },
    removeFile(index) {
      this.pendingFiles.splice(index, 1);
    },
    clearPendingFiles() {
      this.pendingFiles = [];
    },
    async selectSingleFile() {
      const filePath = await ipcRenderer.invoke('select-file');
      if (filePath) {
        const stats = fs.statSync(filePath);
        this.pendingFiles.push({
          name: path.basename(filePath),
          path: filePath,
          size: stats.size
        });
      }
    },
    async convertFiles() {
      if (this.pendingFiles.length === 0) {
        this.$message.error('请选择要转换的文件');
        return;
      }

      this.converting = true;
      this.progressVisible = true;
      this.progress = 0;

      try {
        for (let i = 0; i < this.pendingFiles.length; i++) {
          const file = this.pendingFiles[i];
          const outputPath = this.useCustomOutput ? 
            path.join(this.singleOutput, file.name.replace('.ncm', '.mp3')) :
            file.path.replace('.ncm', '.mp3');

          try {
            await this.convertFile(file.path, outputPath);
            if (this.deleteOriginal) {
              fs.unlinkSync(file.path);
            }
            this.addToHistory({
              inputFile: file.path,
              outputFile: outputPath,
              status: 'success'
            });
          } catch (error) {
            this.addToHistory({
              inputFile: file.path,
              outputFile: outputPath,
              status: 'error',
              error: error.message
            });
          }

          this.progress = Math.round(((i + 1) / this.pendingFiles.length) * 100);
        }

        this.progressStatus = 'success';
        this.$message.success('转换完成');
        this.pendingFiles = [];
      } catch (error) {
        this.progressStatus = 'exception';
        this.$message.error('转换失败: ' + error.message);
      } finally {
        this.converting = false;
      }
    },
    formatDate(timestamp) {
      const date = new Date(timestamp);
      return date.toLocaleString();
    },
    getFileName(filePath) {
      return path.basename(filePath);
    },
    clearHistory() {
      this.conversionHistory = [];
    },
    addToHistory(record) {
      this.conversionHistory.unshift({
        timestamp: Date.now(),
        ...record
      });
    },
    async selectSingleOutput() {
      this.singleOutput = await ipcRenderer.invoke('select-folder');
    },
    async selectBatchInput() {
      this.batchInput = await ipcRenderer.invoke('select-folder');
    },
    async selectBatchOutput() {
      this.batchOutput = await ipcRenderer.invoke('select-folder');
    },
    async convertFile(inputPath, outputPath) {
      return new Promise((resolve, reject) => {
        const isDev = process.env.NODE_ENV === 'development';
        const scriptPath = isDev ? 
          path.join(__dirname, '..', 'ncm_converter.py') :
          path.join(process.resourcesPath, 'ncm_converter.py');

        const options = {
          mode: 'text',
          pythonPath: 'python',
          pythonOptions: ['-u'],
          scriptPath: path.dirname(scriptPath),
          args: [inputPath, outputPath]
        };

        PythonShell.run(path.basename(scriptPath), options).then(messages => {
          if (messages[0] === 'success') {
            resolve();
          } else {
            reject(new Error(messages[0].replace('error:', '')));
          }
        }).catch(err => {
          reject(err);
        });
      });
    },
    async convertBatch() {
      if (!this.batchInput) {
        this.$message.error('请选择输入文件夹');
        return;
      }

      this.converting = true;
      this.progressVisible = true;
      this.progress = 0;

      try {
        const files = fs.readdirSync(this.batchInput)
          .filter(file => file.toLowerCase().endsWith('.ncm'));

        if (files.length === 0) {
          this.$message.warning('没有找到NCM文件');
          return;
        }

        const outputDir = this.useCustomBatchOutput ? this.batchOutput : this.batchInput;

        for (let i = 0; i < files.length; i++) {
          const file = files[i];
          const inputPath = path.join(this.batchInput, file);
          const outputPath = path.join(outputDir, file.replace('.ncm', '.mp3'));

          try {
            await this.convertFile(inputPath, outputPath);
            if (this.deleteBatchOriginal) {
              fs.unlinkSync(inputPath);
            }
            this.addToHistory({
              inputFile: inputPath,
              outputFile: outputPath,
              status: 'success'
            });
          } catch (error) {
            this.addToHistory({
              inputFile: inputPath,
              outputFile: outputPath,
              status: 'error',
              error: error.message
            });
          }
          
          this.progress = Math.round(((i + 1) / files.length) * 100);
        }

        this.progressStatus = 'success';
        this.$message.success('批量转换完成');
      } catch (error) {
        this.progressStatus = 'exception';
        this.$message.error('转换失败: ' + error.message);
      } finally {
        this.converting = false;
      }
    }
  }
}
</script>

<style>
.container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.conversion-form {
  margin-top: 20px;
}

.drop-area {
  border: 2px dashed #dcdfe6;
  border-radius: 6px;
  padding: 40px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  margin-bottom: 20px;
}

.drop-area.is-dragover {
  border-color: #409eff;
  background-color: rgba(64, 158, 255, 0.1);
}

.drop-icon {
  font-size: 48px;
  color: #909399;
  margin-bottom: 16px;
}

.drop-text {
  font-size: 16px;
  color: #606266;
  margin-bottom: 8px;
}

.drop-hint {
  font-size: 12px;
  color: #909399;
}

.file-list {
  margin-top: 20px;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.list-header h4 {
  margin: 0;
  font-size: 16px;
  color: #303133;
}

.conversion-options {
  margin: 20px 0;
  padding: 16px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.action-buttons {
  margin-top: 20px;
  text-align: center;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
}

.history-container {
  margin-top: 20px;
}

.history-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.history-header h3 {
  margin: 0;
}

.error-message {
  color: #f56c6c;
  font-size: 12px;
}

.el-input-group__prepend {
  background-color: #f5f7fa;
  color: #909399;
  padding: 0 15px;
}

.option-row {
  margin-bottom: 12px;
}

.about-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.about-container h2 {
  text-align: center;
  margin-bottom: 8px;
}

.version {
  text-align: center;
  color: #909399;
  margin-bottom: 32px;
}

.section {
  margin-bottom: 32px;
}

.section h3 {
  margin-bottom: 16px;
  padding-bottom: 8px;
  border-bottom: 1px solid #ebeef5;
}

.section h4 {
  margin: 16px 0 8px;
  color: #606266;
}

.section ul, .section ol {
  padding-left: 20px;
  color: #606266;
}

.section li {
  margin-bottom: 8px;
}

.section a {
  color: #409eff;
  text-decoration: none;
}

.section a:hover {
  text-decoration: underline;
}
</style> 