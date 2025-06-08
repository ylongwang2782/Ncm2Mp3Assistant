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
      progressStatus: ''
    }
  },
  methods: {
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
    async checkPythonDependencies() {
      // 不再需要检查 Python 依赖，因为已经打包到可执行文件中
      return true;
    },
    async convertFile(inputPath, outputPath) {
      return new Promise((resolve, reject) => {
        const isDev = process.env.NODE_ENV === 'development';
        const converterPath = isDev ? 
          path.join(__dirname, '..', 'ncm_converter.py') :
          path.join(process.resourcesPath, 'dist_python', 'ncm_converter.exe');

        const options = {
          mode: 'text',
          args: [inputPath, outputPath]
        };

        if (isDev) {
          options.pythonPath = 'python';
          options.pythonOptions = ['-u'];
          options.scriptPath = path.dirname(converterPath);
          PythonShell.run(path.basename(converterPath), options).then(messages => {
            if (messages[0] === 'success') {
              resolve();
            } else {
              reject(new Error(messages[0].replace('error:', '')));
            }
          }).catch(err => {
            reject(err);
          });
        } else {
          const { spawn } = require('child_process');
          const process = spawn(converterPath, [inputPath, outputPath]);
          
          let output = '';
          process.stdout.on('data', (data) => {
            output += data.toString();
          });

          process.stderr.on('data', (data) => {
            output += data.toString();
          });

          process.on('close', (code) => {
            if (code === 0) {
              resolve();
            } else {
              reject(new Error(output || '转换失败'));
            }
          });
        }
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
      } catch (error) {
        this.progressStatus = 'exception';
        this.$message.error('转换失败: ' + error.message);
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

          await this.convertFile(inputPath, outputPath);
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
  max-width: 800px;
  margin: 0 auto;
}

.conversion-form {
  margin-top: 20px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
}
</style> 