<script setup>
import { h, onMounted, ref, reactive } from 'vue'
import {
  NButton,
  NForm,
  NFormItem,
  NInput,
  NPopconfirm,
  NDatePicker,
  NSelect,
  useMessage,
  NModal,
  NTable,
} from 'naive-ui'

import CommonPage from '@/components/page/CommonPage.vue'
import QueryBarItem from '@/components/query-bar/QueryBarItem.vue'
import CrudModal from '@/components/table/CrudModal.vue'
import CrudTable from '@/components/table/CrudTable.vue'

import {useCRUD} from '@/composables'
import api from '@/api'
import TheIcon from '@/components/icon/TheIcon.vue'
import {useUserStore} from '@/store'

defineOptions({name: '赛事管理'})

const message = useMessage()
const $table = ref(null)
const queryItems = ref({})
const dataLoaded = ref(false)

const defaultForm = {
  name: '',
  status: '',
  address: '',
  date: null,
  participants: 0,
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
  name: '赛事',
  initForm: {...defaultForm},
  doCreate: api.createEvent,
  doDelete: api.deleteEvent,
  doUpdate: api.updateEvent,
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
  {title: '赛事名称', key: 'name', width: 150, align: 'center'},
  {title: '赛事状态', key: 'status', width: 100, align: 'center'},
  {title: '比赛地址', key: 'address', width: 200, align: 'center'},
  {title: '比赛日期', key: 'date', width: 120, align: 'center'},
  {title: '报名人数', key: 'participants', width: 100, align: 'center'},
  {
    title: '操作',
    key: 'actions',
    width: 150,
    align: 'center',
    fixed: 'right',
    render(row) {
      return [
        h(
            NButton,
            {
              size: 'small',
              onClick: () => handleViewTeams(row.id),
            },
            {default: () => '查看队伍'}
        ),"  ",
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
                        // icon: renderIcon('material-symbols:delete-outline', {size: 16}),
                      }
                  ),
              default: () => '确定删除该赛事吗?',
            }
        ),
      ]
    },
  },
]

const teamsModalVisible = ref(false)
const currentTeams = ref([])
const athletesModalVisible = ref(false)
const currentAthletes = ref([])

const handleViewTeams = async (eventId) => {
  // 这里应该调用API获取队伍信息
  // currentTeams.value = await api.getTeamsByEventId(eventId)
  currentTeams.value = [
    {name: '队伍1', address: '地址1', leaderName: '领队1', athleteCount: 10},
    {name: '队伍2', address: '地址2', leaderName: '领队2', athleteCount: 15},
  ]
  teamsModalVisible.value = true
}

const handleViewAthletes = (teamId) => {
  // 这里应该调用API获取运动员信息
  // currentAthletes.value = await api.getAthletesByTeamId(teamId)
  currentAthletes.value = [
    {
      name: '运动员1',
      gender: '男',
      poomsaeIndividual: '是',
      poomsaePair: '否',
      poomsaeTeam: '是',
      taekwondoo: '否',
      competitionTeam: '是',
      esports: '否',
      mixedTeamPoomsae: '是',
      competitionIndividual: '是'
    },
    {
      name: '运动员2',
      gender: '女',
      poomsaeIndividual: '否',
      poomsaePair: '是',
      poomsaeTeam: '是',
      taekwondoo: '是',
      competitionTeam: '否',
      esports: '是',
      mixedTeamPoomsae: '否',
      competitionIndividual: '是'
    },
  ]
  athletesModalVisible.value = true
}

</script>

<template>
  <CommonPage show-footer title="赛事管理">
    <template #action>
      <NButton type="primary" @click="handleAdd">
        <TheIcon icon="material-symbols:add" :size="18" class="mr-5"/>
        新建赛事
      </NButton>
    </template>

    <CrudTable
        ref="$table"
        v-model:query-items="queryItems"
        :columns="columns"
        :get-data="api.getEventList"
    >
      <template #queryBar>
        <QueryBarItem label="赛事名称" :label-width="80">
          <NInput
              v-model:value="queryItems.name"
              clearable
              type="text"
              placeholder="请输入赛事名称"
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
        <NFormItem label="赛事名称" path="name"
                   :rule="{ required: true, message: '请输入赛事名称', trigger: ['input', 'blur'] }">
          <NInput v-model:value="modalForm.name" placeholder="请输入赛事名称"/>
        </NFormItem>
        <NFormItem label="赛事状态" path="status">
          <NSelect v-model:value="modalForm.status" :options="[
            { label: '即将开始', value: '即将开始' },
            { label: '已取消', value: '已取消' },
            { label: '进行中', value: '进行中' },
            { label: '已结束', value: '已结束' }
          ]"/>
        </NFormItem>
        <NFormItem label="比赛地址" path="address">
          <NInput v-model:value="modalForm.address" placeholder="请输入比赛地址"/>
        </NFormItem>
        <NFormItem label="比赛日期" path="date">
          <NDatePicker v-model:value="modalForm.date" type="date"/>
        </NFormItem>

      </NForm>
    </CrudModal>

    <NModal v-model:show="teamsModalVisible" title="查看队伍" :mask-closable="false">
      <NTable :columns="[
        { title: '运动队名称', key: 'name' },
        { title: '运动队地址', key: 'address' },
        { title: '领队姓名', key: 'leaderName' },
        { title: '运动员人数', key: 'athleteCount' },
        {
          title: '操作',
          key: 'actions',
          render: (row) => h(NButton, { onClick: () => handleViewAthletes(row.id) }, { default: () => '查看队员' })
        }
      ]" :data="currentTeams"/>
    </NModal>

    <NModal v-model:show="athletesModalVisible" title="已报名运动员" :mask-closable="false">
      <NTable :columns="[
        { title: '姓名', key: 'name' },
        { title: '性别', key: 'gender' },
        { title: '品势个人', key: 'poomsaeIndividual' },
        { title: '品势混双', key: 'poomsaePair' },
        { title: '品势团体', key: 'poomsaeTeam' },
        { title: '太全屋', key: 'taekwondoo' },
        { title: '竞技团体', key: 'competitionTeam' },
        { title: '电子竞技', key: 'esports' },
        { title: '混合团品', key: 'mixedTeamPoomsae' },
        { title: '竞技个人', key: 'competitionIndividual' },
      ]" :data="currentAthletes"/>
      <template #footer>
        <NButton @click="athletesModalVisible = false">关闭</NButton>
      </template>
    </NModal>
  </CommonPage>
</template>