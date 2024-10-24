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

import {renderIcon} from '@/utils'
import {useCRUD} from '@/composables'
import api from '@/api'
import TheIcon from '@/components/icon/TheIcon.vue'

defineOptions({name: '运动员管理'})

const message = useMessage()
const $table = ref(null)
const queryItems = ref({})
const dataLoaded = ref(false)


const defaultForm = {
  name: '',
  id_card: '',
  gender: '',
  // birth_date: '',
  kumite_group: '',
  kata_group: '',
  individual_kumite: '',
  individual_kata: '',
  pair_kata: '',
  team_kata: '',
  mixed_pair_kata: '',
  team_kumite: '',
  multi_team_free_kata: '',
  mixed_team_kata: '',
  // photo: '',
  // fee: ''
};
const {
  modalVisible,
  modalAction,
  modalTitle,
  modalLoading,
  handleAdd,
  handleDelete,
  handleEdit,
  handleSave,
  handleView,
  modalForm,
  modalFormRef,
} = useCRUD({
  name: '运动员',
  initForm: {...defaultForm},
  doCreate: api.createAthlete,
  doDelete: api.deleteAthlete,
  doUpdate: api.updateAthlete,
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
  {title: '姓名', key: 'name', width: 100, align: 'center'},
  {title: '身份证', key: 'id_card', width: 180, align: 'center'},
  {title: '性别', key: 'gender', width: 60, align: 'center'},
  // { title: '出生年月日', key: 'birth_date', width: 100, align: 'center' },
  // {title: '组手组别', key: 'kumite_group', width: 100, align: 'center'},
  // {title: '型组别', key: 'kata_group', width: 100, align: 'center'},
  // { title: '个人组手', key: 'individual_kumite', width: 100, align: 'center' },
  // { title: '个人型', key: 'individual_kata', width: 100, align: 'center' },
  // { title: '双人型', key: 'pair_kata', width: 100, align: 'center' },
  // { title: '团体型', key: 'team_kata', width: 100, align: 'center' },
  // { title: '混合双人型', key: 'mixed_pair_kata', width: 120, align: 'center' },
  // { title: '团体组手', key: 'team_kumite', width: 100, align: 'center' },
  // { title: '多人团体自由型', key: 'multi_team_free_kata', width: 140, align: 'center' },
  // { title: '混合团体型', key: 'mixed_team_kata', width: 120, align: 'center' },
  // { title: '费用', key: 'fee', width: 80, align: 'center' },
  {
    title: '操作',
    key: 'actions',
    width: 200, // 增加宽度以容纳新按钮
    align: 'center',
    fixed: 'right',
    render(row) {
      return [
        h(
            NButton,
            {
              size: 'small',
              text: true,
              type: 'info',
              style: 'margin-right: 16px;',
              onClick: () => handleView(row)
            },
            {
              default: () => '查看详情',
              icon: renderIcon('material-symbols:visibility-outline', {size: 16}),
            }
        ),
        h(
            NButton,
            {
              size: 'small',
              text: true,
              type: 'primary',
              style: 'margin-right: 16px;',
              onClick: () => handleEdit(row)
            },
            {
              default: () => '编辑',
              icon: renderIcon('material-symbols:edit-outline', {size: 16}),
            }
        ),
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
                        text: true,
                        type: 'error',
                      },
                      {
                        default: () => '删除',
                        icon: renderIcon('material-symbols:delete-outline', {size: 16}),
                      }
                  ),
              default: () => '确定删除该运动员吗?',
            }
        ),
      ]
    },
  },
]


const validateIdCard = (rule, value) => {
  const reg = /(^\d{15}$)|(^\d{18}$)|(^\d{17}(\d|X|x)$)/;
  if (value && !reg.test(value)) {
    return new Error('请输入正确的身份证号码');
  }
  return true;
};
const idCardRules = [
  {required: true, message: '请输入身份证', trigger: ['input', 'blur']},
  {validator: validateIdCard, trigger: ['input', 'blur']}
];

const updateGender = () => {
  const idCard = modalForm.value.id_card;
  if (idCard.length >= 17) {
    const genderCode = parseInt(idCard.charAt(idCard.length - 2));
    modalForm.value.gender = genderCode % 2 === 1 ? '男' : '女';
  } else {
    modalForm.value.gender = '';
  }
};

// 监听身份证输入变化
watch(() => modalForm.value.id_card, updateGender);

</script>

<template>
  <CommonPage show-footer title="运动员管理">
    <template #action>
      <NButton type="primary" @click="handleAdd">
        <TheIcon icon="material-symbols:add" :size="18" class="mr-5"/>
        新建运动员
      </NButton>
    </template>

    <CrudTable
        ref="$table"
        v-model:query-items="queryItems"
        :columns="columns"
        :get-data="api.getAthleteList"
    >
      <template #queryBar>
        <QueryBarItem label="姓名" :label-width="80">
          <NInput
              v-model:value="queryItems.name"
              clearable
              type="text"
              placeholder="请输入姓名"
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
        <NGrid :cols="24" :x-gap="24">
          <NGi :span="12">
            <NFormItem label="姓名" path="name"
                       :rule="{ required: true, message: '请输入姓名', trigger: ['input', 'blur'] }">
              <NInput v-model:value="modalForm.name" placeholder="请输入姓名"/>
            </NFormItem>
          </NGi>
          <NGi :span="8">
            <NFormItem label="性别" path="gender">
              <NSelect
                  v-model:value="modalForm.gender"
                  :options="[
                { label: '男', value: '男' },
                { label: '女', value: '女' }
              ]"
                  placeholder="请选择性别"
                  :disabled="true"
              />
            </NFormItem>
          </NGi>
          <!--          <NGi :span="12">-->
          <!--            <NFormItem label="组手组别" path="kumite_group">-->
          <!--              <NSelect v-model:value="modalForm.kumite_group" :options="[-->
          <!--              { label: '甲组', value: '甲组' },-->
          <!--              { label: '乙组', value: '乙组' },-->
          <!--              { label: '丙A组', value: '丙A组' },-->
          <!--              { label: '丙B组', value: '丙B组' }-->
          <!--            ]" placeholder="请选择组手组别"/>-->
          <!--            </NFormItem>-->
          <!--          </NGi>-->
          <!--          <NGi :span="12">-->
          <!--            <NFormItem label="型组别" path="kata_group">-->
          <!--              <NSelect v-model:value="modalForm.kata_group" :options="[-->
          <!--              { label: '甲组', value: '甲组' },-->
          <!--              { label: '乙组', value: '乙组' },-->
          <!--              { label: '丙A组', value: '丙A组' },-->
          <!--              { label: '丙B组', value: '丙B组' }-->
          <!--            ]" placeholder="请选择型组别"/>-->
          <!--            </NFormItem>-->
          <!--          </NGi>-->
          <!--          <NGi :span="12">-->
          <!--            <NFormItem label="个人组手" path="individual_kumite">-->
          <!--              <NSelect v-model:value="modalForm.individual_kumite" :options="[-->
          <!--              { label: '-67kg', value: '-67kg' },-->
          <!--              { label: '不参赛', value: '不参赛' }-->
          <!--            ]" placeholder="请选择个人组手"/>-->
          <!--            </NFormItem>-->
          <!--          </NGi>-->
          <!--          <NGi :span="12">-->
          <!--            <NFormItem label="个人型" path="individual_kata">-->
          <!--              <NSelect v-model:value="modalForm.individual_kata" :options="[-->
          <!--              { label: '参赛', value: '参赛' },-->
          <!--              { label: '不参赛', value: '不参赛' }-->
          <!--            ]" placeholder="请选择个人型"/>-->
          <!--            </NFormItem>-->
          <!--          </NGi>-->
          <!--          <NGi :span="12">-->
          <!--            <NFormItem label="双人型" path="pair_kata">-->
          <!--              <NSelect v-model:value="modalForm.pair_kata" :options="[-->
          <!--              { label: '清远组', value: '清远组' },-->
          <!--              { label: '不参赛', value: '不参赛' }-->
          <!--            ]" placeholder="请选择双人型"/>-->
          <!--            </NFormItem>-->
          <!--          </NGi>-->
          <!--          <NGi :span="12">-->
          <!--            <NFormItem label="团体型" path="team_kata">-->
          <!--              <NSelect v-model:value="modalForm.team_kata" :options="[-->
          <!--              { label: '第3组', value: '第3组' },-->
          <!--              { label: '不参赛', value: '不参赛' }-->
          <!--            ]" placeholder="请选择团体型"/>-->
          <!--            </NFormItem>-->
          <!--          </NGi>-->
          <!--          <NGi :span="12">-->
          <!--            <NFormItem label="混合双人型" path="mixed_pair_kata">-->
          <!--              <NSelect v-model:value="modalForm.mixed_pair_kata" :options="[-->
          <!--              { label: '第1组', value: '第1组' },-->
          <!--              { label: '不参赛', value: '不参赛' }-->
          <!--            ]" placeholder="请选择混合双人型"/>-->
          <!--            </NFormItem>-->
          <!--          </NGi>-->
          <!--          <NGi :span="12">-->
          <!--            <NFormItem label="团体组手" path="team_kumite">-->
          <!--              <NSelect v-model:value="modalForm.team_kumite" :options="[-->
          <!--              { label: '第2组', value: '第2组' },-->
          <!--              { label: '不参赛', value: '不参赛' }-->
          <!--            ]" placeholder="请选择团体组手"/>-->
          <!--            </NFormItem>-->
          <!--          </NGi>-->
          <!--          <NGi :span="12">-->
          <!--            <NFormItem label="多人团体自由型" path="multi_team_free_kata">-->
          <!--              <NSelect v-model:value="modalForm.multi_team_free_kata" :options="[-->
          <!--              { label: '第1组', value: '第1组' },-->
          <!--              { label: '不参赛', value: '不参赛' }-->
          <!--            ]" placeholder="请选择多人团体自由型"/>-->
          <!--            </NFormItem>-->
          <!--          </NGi>-->
          <!--          <NGi :span="12">-->
          <!--            <NFormItem label="混合团体型" path="mixed_team_kata">-->
          <!--              <NSelect v-model:value="modalForm.mixed_team_kata" :options="[-->
          <!--              { label: '第1组', value: '第1组' },-->
          <!--              { label: '不参赛', value: '不参赛' }-->
          <!--            ]" placeholder="请选择混合团体型"/>-->
          <!--            </NFormItem>-->
          <!--          </NGi>-->
        </NGrid>
        <NGrid :cols="24" :x-gap="24">
          <NGi :span="14">
            <NFormItem label="身份证" path="id_card" :rule="idCardRules">
              <NInput v-model:value="modalForm.id_card" placeholder="请输入身份证" @input="updateGender"/>
            </NFormItem>
          </NGi>
        </NGrid>

        <NGrid :cols="24" :x-gap="24">

          <NGi :span="24">
            <NFormItem label="照片上传" path="photo">
              <NUpload
                  v-model:file-list="modalForm.photo"
                  list-type="image-card"
                  :max="1"
                  accept="image/*"
              >
                点击上传
              </NUpload>
            </NFormItem>
          </NGi>
        </NGrid>


      </NForm>
    </CrudModal>
  </CommonPage>
</template>