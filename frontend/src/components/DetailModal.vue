<template>
  <TransitionRoot appear as="template" :show="true">
    <Dialog as="div" class="fixed inset-0 z-10 overflow-y-auto" @close="close">
      <div class="flex items-center justify-center min-h-screen px-4 text-center">
        <DialogOverlay class="fixed inset-0 bg-black bg-opacity-50" />
        <span class="inline-block h-screen align-middle" aria-hidden="true">&#8203;</span>
        <TransitionChild
          as="template"
          enter="ease-out duration-300"
          enter-from="opacity-0 scale-95"
          enter-to="opacity-100 scale-100"
          leave="ease-in duration-200"
          leave-from="opacity-100 scale-100"
          leave-to="opacity-0 scale-95"
        >
          <div class="inline-block w-full max-w-md p-6 my-8 overflow-hidden text-left align-middle bg-card-dark shadow-xl rounded-lg">
            <DialogTitle class="text-lg font-bold leading-6 text-text-light">
              <slot name="title" />
            </DialogTitle>
            <div class="mt-4 text-text-light space-y-2">
              <slot name="body" />
            </div>
            <div class="mt-6 text-right">
              <button @click="close" class="btn-primary">Close</button>
            </div>
          </div>
        </TransitionChild>
      </div>
    </Dialog>
  </TransitionRoot>
</template>

<script setup>
import { emit } from 'vue'
import { Dialog, DialogOverlay, DialogTitle, TransitionRoot, TransitionChild } from '@headlessui/vue'
const emitClose = defineEmits(['close'])
function close() {
  emitClose('close')
}
</script>
