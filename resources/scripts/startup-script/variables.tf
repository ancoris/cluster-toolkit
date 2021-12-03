/**
 * Copyright 2021 Google LLC
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

variable "deployment_name" {
  description = "Name of the HPC deployment, used to name GCS bucket for startup scripts."
  type        = string
}

variable "region" {
  description = "The region to deploy to"
  type        = string
}


variable "runners" {
  description = <<EOT
    List of runners to run on remote VM.
    Runners can be of type ansible, shell or data.
    {
      type: ansible-local || shell
      spec: {
        file: <file path>
      } || {
        name: <name of destination script>
        content: <text content of the script>
      }
    } || {
      type: data
      spec: {
        dir: <folder to be compressed and uploaded with `tar zcf`>
        dest_path: <path where expanded at destination>
        runnable: <null or script to run after `tar zxf`>
      }
EOT
  type        = list(map(string))
  validation {
    condition = alltrue([
      for o in var.runners : contains(keys(o), "type")
    ])
    error_message = "All runners must declare a type."
  }
  validation {
    condition = alltrue([
      for o in var.runners : o["type"] == "ansible-local" || o["type"] == "shell"
    ])
    error_message = "The 'type' must be 'ansible-local' or 'shell'."
  }
  validation {
    condition = alltrue([
      for o in var.runners : (contains(keys(o), "file") &&
      !contains(keys(o), "content") && !contains(keys(o), "name")) ||
      (!contains(keys(o), "file")
      && contains(keys(o), "content") && contains(keys(o), "name"))
    ])
    error_message = "Invalid runner: 'filename' cannot be specified with 'name' and 'content'."
  }
  # validation {
  #   condition = alltrue([
  #     for o in var.runners : contains(keys(o.spec),"file") || (contains(keys(o.spec),"name") && contains(key(o.spec),"content")
  #   ])
  #   error_message = "Type can only be 'ansible-local' or 'shell'."
  # }
  default = []
}
