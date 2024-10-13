<script setup>
import {h, onMounted, ref, reactive} from 'vue'
import {
  NButton,
  NForm,
  NFormItem,
  NInput,
  NPopconfirm,
  NUpload,
  NGrid,
  NGi,
  useMessage,
} from 'naive-ui'

import CommonPage from '@/components/page/CommonPage.vue'
import QueryBarItem from '@/components/query-bar/QueryBarItem.vue'
import CrudModal from '@/components/table/CrudModal.vue'
import CrudTable from '@/components/table/CrudTable.vue'

import {formatDate, renderIcon} from '@/utils'
import {useCRUD} from '@/composables'
import api from '@/api'
import TheIcon from '@/components/icon/TheIcon.vue'
import { useUserStore } from '@/store'

defineOptions({name: '运动队管理'})

const message = useMessage()
const $table = ref(null)
const queryItems = ref({})
const dataLoaded = ref(false)


const userStore = useUserStore()

console.log(userStore.userId)
console.log(userStore.userInfo)

const defaultForm = {
  name: '',
  short_name: '',
  address: '',
  leader_name: '',
  leader_phone: '',
  leader_photo: [],
  doctor_name: '',
  doctor_phone: '',
  staff_name: '',
  staff_phone: '',
  coaches1: '',
  coaches2: '',
  coaches1_phone: '',
  coaches2_phone: '',
}

const {
  modalVisible,
  modalAction,
  modalTitle,
  modalLoading,
  handleAdd,
  handleDelete,
  handleEdit,
  handleSave,
  modalForm,
  modalFormRef,
} = useCRUD({
  name: '运动队',
  initForm: {...defaultForm},
  doCreate: api.createTeam,
  doDelete: api.deleteTeam,
  doUpdate: api.updateTeam,
  refresh: () => $table.value?.handleSearch(),
})

onMounted(async () => {
  try {
    await $table.value?.handleSearch()
    dataLoaded.value = true
  } catch (error) {
    console.error('Failed to load initial data:', error)
    message.error('加载数据失败，请刷新页面重试')
  }
})

const columns = [
  {title: '运动队名称', key: 'name', width: 150, align: 'center'},
  {title: '地址', key: 'address', width: 200, align: 'center'},
  {title: '领队名称', key: 'leader_name', width: 100, align: 'center'},
  {title: '领队联系方式', key: 'leader_phone', width: 100, align: 'center'},
  {
    title: '操作',
    key: 'actions',
    width: 100,
    align: 'center',
    fixed: 'right',
    render(row) {
      return [
        // h(
        //     NButton,
        //     {
        //       size: 'small',
        //       type: 'primary',
        //       style: 'margin-right: 8px;',
        //       onClick: () => handleEdit(row),
        //     },
        //     {default: () => '编辑', icon: renderIcon('material-symbols:edit-outline', {size: 16})}
        // ),
        h(
            NPopconfirm,
            {
              onPositiveClick: () => handleDelete({id: row.id}),
            },
            {
              trigger: () =>
                  h(
                      NButton,
                      {
                        size: 'small',
                        type: 'error',
                      },
                      {
                        default: () => '删除',
                        icon: renderIcon('material-symbols:delete-outline', {size: 16}),
                      }
                  ),
              default: () => '确定删除该运动队吗?',
            }
        ),
      ]
    },
  },
]

</script>

<template>
  <CommonPage show-footer title="运动队管理">
    <template #action>
      <NButton type="primary" @click="handleAdd">
        <TheIcon icon="material-symbols:add" :size="18" class="mr-5"/>
        新建运动队
      </NButton>
    </template>

    <CrudTable
        ref="$table"
        v-model:query-items="queryItems"
        :columns="columns"
        :get-data="api.getTeamList"
    >
      <template #queryBar>
        <QueryBarItem label="运动队名称" :label-width="80">
          <NInput
              v-model:value="queryItems.name"
              clearable
              type="text"
              placeholder="请输入运动队名称"
              @keypress.enter="$table?.handleSearch()"
          />
        </QueryBarItem>
      </template>
    </CrudTable>

    <CrudModal
        v-model:visible="modalVisible"
        :title="modalTitle"
        :loading="modalLoading"
        @save="handleSave"
        :width="1"
    >
      <NForm
          v-if="modalForm"
          ref="modalFormRef"
          label-placement="left"
          label-align="left"
          :label-width="100"
          :model="modalForm"
          :disabled="modalAction === 'view'"
      >
        <NGrid :cols="24" :x-gap="24">
          <NGi :span="12">
            <NFormItem label="运动队名称" path="name"
                       :rule="{ required: true, message: '请输入运动队名称', trigger: ['input', 'blur'] }">
              <NInput v-model:value="modalForm.name" placeholder="请输入运动队名称"/>
            </NFormItem>
          </NGi>
          <NGi :span="12">
            <NFormItem label="运动队简称" path="short_name">
              <NInput v-model:value="modalForm.short_name" placeholder="请输入运动队简称"/>
            </NFormItem>
          </NGi>
        </NGrid>
        <NFormItem label="地址" path="address">
          <NInput v-model:value="modalForm.address" placeholder="请输入地址"/>
        </NFormItem>
        <NGrid :cols="24" :x-gap="24">
          <NGi :span="8">
            <NFormItem label="领队名称" path="leader_name">
              <NInput v-model:value="modalForm.leader_name" placeholder="请输入领队名称"/>
            </NFormItem>
          </NGi>
          <NGi :span="8">
            <NFormItem label="领队电话" path="leader_phone">
              <NInput v-model:value="modalForm.leader_phone" placeholder="请输入领队电话"/>
            </NFormItem>
          </NGi>
          <NGi :span="8">
            <NFormItem label="领队照片" path="leader_photo">
              <NUpload
                  v-model:file-list="modalForm.leader_photo"
                  list-type="image-card"
                  :max="1"
              />
            </NFormItem>
          </NGi>
        </NGrid>
        <NGrid :cols="24" :x-gap="24">
          <NGi :span="12">
            <NFormItem label="队医姓名" path="doctor_name">
              <NInput v-model:value="modalForm.doctor_name" placeholder="请输入队医姓名"/>
            </NFormItem>
          </NGi>
          <NGi :span="12">
            <NFormItem label="队医电话" path="doctor_phone">
              <NInput v-model:value="modalForm.doctor_phone" placeholder="请输入队医电话"/>
            </NFormItem>
          </NGi>
        </NGrid>
        <NGrid :cols="24" :x-gap="24">
          <NGi :span="12">
            <NFormItem label="工作人员姓名" path="staff_name">
              <NInput v-model:value="modalForm.staff_name" placeholder="请输入工作人员姓名"/>
            </NFormItem>
          </NGi>
          <NGi :span="12">
            <NFormItem label="工作人员电话" path="staff_phone">
              <NInput v-model:value="modalForm.staff_phone" placeholder="请输入工作人员电话"/>
            </NFormItem>
          </NGi>
        </NGrid>

        <NGrid :cols="24" :x-gap="24">
          <NGi :span="12">
            <NFormItem label="教练员1" path="coaches1">
              <NInput v-model:value="modalForm.coaches1" placeholder="请输入工作人员姓名"/>
            </NFormItem>
          </NGi>
          <NGi :span="12">
            <NFormItem label="教练员1电话" path="coaches1_phone">
              <NInput v-model:value="modalForm.coaches1_phone" placeholder="请输入工作人员电话"/>
            </NFormItem>
          </NGi>
        </NGrid>

        <NGrid :cols="24" :x-gap="24">
          <NGi :span="12">
            <NFormItem label="教练员2" path="coaches2">
              <NInput v-model:value="modalForm.coaches2" placeholder="请输入工作人员姓名"/>
            </NFormItem>
          </NGi>
          <NGi :span="12">
            <NFormItem label="教练员2电话" path="coaches2_phone">
              <NInput v-model:value="modalForm.coaches2_phone" placeholder="请输入工作人员电话"/>
            </NFormItem>
          </NGi>
        </NGrid>
      </NForm>
    </CrudModal>
  </CommonPage>
</template>