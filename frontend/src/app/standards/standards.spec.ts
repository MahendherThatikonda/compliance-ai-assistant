import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Standards } from './standards';

describe('Standards', () => {
  let component: Standards;
  let fixture: ComponentFixture<Standards>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Standards],
    }).compileComponents();

    fixture = TestBed.createComponent(Standards);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
