<template>
  <div class="container">
    <el-tabs v-model="activeTab">
      <el-tab-pane label="单个转换" name="single">
        <div class="conversion-form">
          <el-form label-position="top">
            <el-form-item label="输入文件">
              <el-input v-model="singleInput" readonly>
                <template #append>
                  <el-button @click="selectSingleFile">浏览</el-button>
                </template>
              </el-input>
            </el-form-item>
            
            <el-form-item label="输出位置">
              <el-checkbox v-model="useCustomOutput">自定义输出位置</el-checkbox>
              <el-input v-model="singleOutput" readonly v-if="useCustomOutput">
                <template #append>
                  <el-button @click="selectSingleOutput">浏览</el-button>
                </template>
              </el-input>
            </el-form-item>

            <el-form-item>
              <el-button type="primary" @click="convertSingle" :loading="converting">
                开始转换
              </el-button>
            </el-form-item>
          </el-form>
        </div>
      </el-tab-pane>

      <el-tab-pane label="批量转换" name="batch">
        <div class="conversion-form">
          <el-form label-position="top">
            <el-form-item label="输入文件夹">
              <el-input v-model="batchInput" readonly>
                <template #append>
                  <el-button @click="selectBatchInput">浏览</el-button>
                </template>
              </el-input>
            </el-form-item>
            
            <el-form-item label="输出文件夹">
              <el-checkbox v-model="useCustomBatchOutput">自定义输出位置</el-checkbox>
              <el-input v-model="batchOutput" readonly v-if="useCustomBatchOutput">
                <template #append>
                  <el-button @click="selectBatchOutput">浏览</el-button>
                </template>
              </el-input>
            </el-form-item>

            <el-form-item>
              <el-button type="primary" @click="convertBatch" :loading="converting">
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

export default {
  name: 'App',
  data() {
    return {
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
      conversionHistory: []
    }
  },
  computed: {
    hasErrors() {
      return this.conversionHistory.some(record => record.error);
    }
  },
  methods: {
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
    async selectSingleFile() {
      this.singleInput = await ipcRenderer.invoke('select-file');
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
    async convertSingle() {
      if (!this.singleInput) {
        this.$message.error('请选择输入文件');
        return;
      }

      this.converting = true;
      this.progressVisible = true;
      this.progress = 0;

      try {
        const outputPath = this.useCustomOutput ? 
          path.join(this.singleOutput, path.basename(this.singleInput, '.ncm') + '.mp3') :
          this.singleInput.replace('.ncm', '.mp3');

        await this.convertFile(this.singleInput, outputPath);
        this.progress = 100;
        this.progressStatus = 'success';
        this.$message.success('转换完成');
        this.addToHistory({
          inputFile: this.singleInput,
          outputFile: outputPath,
          status: 'success'
        });
      } catch (error) {
        this.progressStatus = 'exception';
        this.$message.error('转换失败: ' + error.message);
        this.addToHistory({
          inputFile: this.singleInput,
          outputFile: this.singleInput.replace('.ncm', '.mp3'),
          status: 'error',
          error: error.message
        });
      } finally {
        this.converting = false;
      }
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
</style> 