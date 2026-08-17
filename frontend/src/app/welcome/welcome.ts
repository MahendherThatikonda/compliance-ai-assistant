// src/app/welcome/welcome.ts

import {
  Component,
  EventEmitter,
  Input,
  Output
} from '@angular/core';

import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-welcome',
  standalone: true,
  imports: [
    CommonModule
  ],
  templateUrl: './welcome.html',
  styleUrl: './welcome.css'
})
export class Welcome {

  @Input()
  examples: string[] = [];

  @Output()
  exampleSelected = new EventEmitter<string>();


  selectExample(example: string) {
    this.exampleSelected.emit(example);
  }

}